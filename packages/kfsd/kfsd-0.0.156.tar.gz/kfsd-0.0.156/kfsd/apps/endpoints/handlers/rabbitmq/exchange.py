from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.rabbitmq.exchange import (
    ExchangeModelSerializer,
    ExchangeViewModelSerializer,
)

from kfsd.apps.models.tables.rabbitmq.exchange import Exchange


def gen_exchange_handler(instance):
    handler = ExchangeHandler(instance.identifier, False)
    qsData = ExchangeModelSerializer(instance=instance)
    handler.setModelQSRawData(qsData)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


@receiver(post_save, sender=Exchange)
def process_post_save(sender, instance, created, **kwargs):
    pass


@receiver(post_delete, sender=Exchange)
def process_post_del(sender, instance, **kwargs):
    pass


class ExchangeHandler(BaseHandler):
    def __init__(self, exchangeIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=ExchangeModelSerializer,
            viewSerializer=ExchangeViewModelSerializer,
            modelClass=Exchange,
            identifier=exchangeIdentifier,
            isDBFetch=isDBFetch,
        )
