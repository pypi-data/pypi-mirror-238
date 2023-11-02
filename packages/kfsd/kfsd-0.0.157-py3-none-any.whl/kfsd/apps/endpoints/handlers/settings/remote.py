from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.settings.remote import (
    RemoteModelSerializer,
    RemoteViewModelSerializer,
)
from kfsd.apps.endpoints.handlers.requests.endpoint import gen_endpoint_handler

from kfsd.apps.models.tables.settings.remote import Remote


def gen_remote_handler(instance):
    handler = RemoteHandler(instance.identifier, False)
    qsData = RemoteModelSerializer(instance=instance)
    handler.setModelQSRawData(qsData)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


@receiver(post_save, sender=Remote)
def process_post_save(sender, instance, created, **kwargs):
    pass


@receiver(post_delete, sender=Remote)
def process_post_del(sender, instance, **kwargs):
    pass


class RemoteHandler(BaseHandler):
    DIMENSIONS_KEY = "dimensions"

    def __init__(self, remoteIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=RemoteModelSerializer,
            viewSerializer=RemoteViewModelSerializer,
            modelClass=Remote,
            identifier=remoteIdentifier,
            isDBFetch=isDBFetch,
        )

    def getEndpointHandler(self):
        return gen_endpoint_handler(self.getModelQS().endpoint)

    def genConfig(self, dimensions):
        return self.getEndpointHandler().exec({self.DIMENSIONS_KEY: dimensions}).json()
