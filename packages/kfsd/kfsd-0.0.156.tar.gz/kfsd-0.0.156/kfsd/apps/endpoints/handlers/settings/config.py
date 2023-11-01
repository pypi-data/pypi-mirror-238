from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.handlers.settings.local import gen_local_handler
from kfsd.apps.endpoints.handlers.settings.remote import gen_remote_handler
from kfsd.apps.endpoints.serializers.settings.config import (
    ConfigModelSerializer,
    ConfigViewModelSerializer,
)

from kfsd.apps.models.tables.settings.config import Config

from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.utils.system import System


def gen_config_handler(instance):
    handler = ConfigHandler(instance.identifier, False)
    qsData = ConfigModelSerializer(instance=instance)
    handler.setModelQSRawData(qsData)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


@receiver(post_save, sender=Config)
def process_post_save(sender, instance, created, **kwargs):
    pass


@receiver(post_delete, sender=Config)
def process_post_del(sender, instance, **kwargs):
    pass


class ConfigHandler(BaseHandler):
    def __init__(self, configIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=ConfigModelSerializer,
            viewSerializer=ConfigViewModelSerializer,
            modelClass=Config,
            identifier=configIdentifier,
            isDBFetch=isDBFetch,
        )

    def isLocalConfig(self):
        return DictUtils.get(self.getModelQSData(), "is_local_config")

    def getLookupDimensions(self):
        return DictUtils.get(self.getModelQSData(), "lookup_dimension_keys")

    def getLocalHandler(self):
        return gen_local_handler(self.getModelQS().local)

    def getRemoteHandler(self):
        return gen_remote_handler(self.getModelQS().remote)

    def genConfig(self):
        if self.isLocalConfig():
            return self.getLocalHandler().genConfig(self.constructDimensionsFromEnv())
        else:
            return self.getRemoteHandler().genConfig(self.constructDimensionsFromEnv())

    def constructDimensionsFromEnv(self):
        return {key: System.getEnv(key) for key in self.getLookupDimensions()}
