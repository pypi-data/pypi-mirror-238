from functools import wraps

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from kfsd.apps.endpoints.handlers.signals.base import BaseSignalHandler
from kfsd.apps.endpoints.serializers.signals.outbound import (
    OutboundModelSerializer,
    OutboundViewModelSerializer,
)

from kfsd.apps.models.tables.signals.outbound import Outbound
from kfsd.apps.models.constants import ENV_OUTBOUND_POLICY_ID, ENV_SERVICE_ID

from kfsd.apps.core.utils.system import System
from kfsd.apps.core.common.logger import Logger, LogLevel

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


def add_outbound_signal(data):
    logger.debug("[OUTBOUND DATA]: {}".format(data))
    Outbound.objects.create(data=data)


def gen_correlation_id():
    return System.uuid(32)


def getAppName():
    return System.getEnv(ENV_SERVICE_ID)


def getEventMeta(kwargs):
    tblName = kwargs["sender"].__name__
    serviceId = getAppName()
    op = "CREATE"
    if "created" in kwargs:
        if not kwargs["created"]:
            op = "UPDATE"
    else:
        op = "DELETE"
    return {"op": op, "service_id": serviceId, "tbl": tblName}


def gen_upsert_event(func, kwargs):
    handler = func(kwargs["instance"])
    viewData = handler.getViewModelQSData()
    eventMeta = getEventMeta(kwargs)
    eventData = {
        "type": "upsert",
        "correlation_id": gen_correlation_id(),
        "meta": eventMeta,
        "attrs": viewData,
    }
    add_outbound_signal(eventData)


def upsert_tbl_event(get_instance_handler):
    def exec(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            gen_upsert_event(get_instance_handler, kwargs)
            data = func(*args, **kwargs)
            return data

        return wrapper

    return exec


def gen_outbound_handler(instance):
    handler = OutboundHandler(instance.identifier, False)
    qsData = OutboundModelSerializer(instance=instance)
    handler.setModelQSRawData(qsData)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


def process_outbound_signal(instance):
    inboundHandler = gen_outbound_handler(instance)
    inboundHandler.exec()


@receiver(post_save, sender=Outbound)
def process_post_save(sender, instance, created, **kwargs):
    if created:
        process_outbound_signal(instance)


@receiver(post_delete, sender=Outbound)
def process_post_del(sender, instance, **kwargs):
    pass


class OutboundHandler(BaseSignalHandler):
    def __init__(self, outboundIdentifier, isDBFetch):
        BaseSignalHandler.__init__(
            self,
            serializer=OutboundModelSerializer,
            viewSerializer=OutboundViewModelSerializer,
            modelClass=Outbound,
            identifier=outboundIdentifier,
            isDBFetch=isDBFetch,
            env_policy_id=ENV_OUTBOUND_POLICY_ID,
        )

    @staticmethod
    def clear():
        inboundQS = Outbound.objects.filter(status="E").order_by("created")
        for instance in inboundQS:
            process_outbound_signal(instance)
        return {"detail": "success"}
