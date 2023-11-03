from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.settings.local import (
    LocalModelSerializer,
    LocalViewModelSerializer,
)

from kfsd.apps.models.tables.settings.local import Local

from kfsd.apps.core.common.configuration import Configuration
from kfsd.apps.core.utils.dict import DictUtils


def gen_local_handler(instance):
    handler = LocalHandler(instance.identifier, False)
    qsData = LocalModelSerializer(instance=instance)
    handler.setModelQSRawData(qsData)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


@receiver(post_save, sender=Local)
def process_post_save(sender, instance, created, **kwargs):
    pass


@receiver(post_delete, sender=Local)
def process_post_del(sender, instance, **kwargs):
    pass


class LocalHandler(BaseHandler):
    def __init__(self, localIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=LocalModelSerializer,
            viewSerializer=LocalViewModelSerializer,
            modelClass=Local,
            identifier=localIdentifier,
            isDBFetch=isDBFetch,
        )

    def getData(self):
        return DictUtils.get(self.getModelQSData(), "data")

    def genConfig(self, dimensions):
        config = Configuration(
            settings=self.getData(), dimensions=dimensions
        ).getFinalConfig()
        return config
