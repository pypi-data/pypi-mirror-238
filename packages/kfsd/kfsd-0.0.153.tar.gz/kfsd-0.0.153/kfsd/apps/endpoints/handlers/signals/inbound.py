from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from kfsd.apps.endpoints.serializers.signals.inbound import (
    InboundModelSerializer,
    InboundViewModelSerializer,
)
from kfsd.apps.endpoints.handlers.signals.base import BaseSignalHandler

from kfsd.apps.models.tables.signals.inbound import Inbound
from kfsd.apps.models.constants import ENV_INBOUND_POLICY_ID

from kfsd.apps.core.common.logger import Logger, LogLevel

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


def gen_inbound_handler(instance):
    handler = InboundHandler(instance.identifier, False)
    qsData = InboundModelSerializer(instance=instance)
    handler.setModelQSRawData(qsData)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


def add_inbound_signal(data):
    logger.debug("[INBOUND DATA]: {}".format(data))
    Inbound.objects.create(data=data)


def process_inbound_signal(instance):
    inboundHandler = gen_inbound_handler(instance)
    inboundHandler.exec()


@receiver(post_save, sender=Inbound)
def process_post_save(sender, instance, created, **kwargs):
    if created:
        process_inbound_signal(instance)


@receiver(post_delete, sender=Inbound)
def process_post_del(sender, instance, **kwargs):
    pass


class InboundHandler(BaseSignalHandler):
    def __init__(self, inboundIdentifier, isDBFetch):
        BaseSignalHandler.__init__(
            self,
            serializer=InboundModelSerializer,
            viewSerializer=InboundViewModelSerializer,
            modelClass=Inbound,
            identifier=inboundIdentifier,
            isDBFetch=isDBFetch,
            env_policy_id=ENV_INBOUND_POLICY_ID,
        )

    @staticmethod
    def clear():
        inboundQS = Inbound.objects.filter(status="E").order_by("created")
        for instance in inboundQS:
            process_inbound_signal(instance)
        return {"detail": "success"}
