from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from kfsd.apps.endpoints.handlers.settings.config import gen_config_handler
from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.settings.setting import (
    SettingModelSerializer,
    SettingViewModelSerializer,
)

from kfsd.apps.models.tables.settings.setting import Setting

from kfsd.apps.core.utils.dict import DictUtils


def gen_setting_handler(instance):
    handler = SettingHandler(instance.identifier, False)
    qsData = SettingModelSerializer(instance=instance)
    handler.setModelQSRawData(qsData)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


@receiver(post_save, sender=Setting)
def process_post_save(sender, instance, created, **kwargs):
    pass


@receiver(post_delete, sender=Setting)
def process_post_del(sender, instance, **kwargs):
    pass


class SettingHandler(BaseHandler):
    def __init__(self, settingIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=SettingModelSerializer,
            viewSerializer=SettingViewModelSerializer,
            modelClass=Setting,
            identifier=settingIdentifier,
            isDBFetch=isDBFetch,
        )

    def getConfigId(self):
        return DictUtils.get(self.getModelQSData(), "config")

    def getConfigHandler(self):
        return gen_config_handler(self.getModelQS().config)

    def genConfig(self):
        return self.getConfigHandler().genConfig()
