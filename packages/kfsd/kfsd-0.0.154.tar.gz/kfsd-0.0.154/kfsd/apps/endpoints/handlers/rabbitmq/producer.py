from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.rabbitmq.producer import (
    ProducerModelSerializer,
    ProducerViewModelSerializer,
)

from kfsd.apps.models.tables.rabbitmq.producer import Producer

from kfsd.apps.core.msmq.rabbitmq.base import RabbitMQ


def gen_producer_handler(instance):
    handler = ProducerHandler(instance.identifier, False)
    qsData = ProducerModelSerializer(instance=instance)
    handler.setModelQSRawData(qsData)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


@receiver(post_save, sender=Producer)
def process_post_save(sender, instance, created, **kwargs):
    pass


@receiver(post_delete, sender=Producer)
def process_post_del(sender, instance, **kwargs):
    pass


class ProducerHandler(BaseHandler):
    def __init__(self, producerIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=ProducerModelSerializer,
            viewSerializer=ProducerViewModelSerializer,
            modelClass=Producer,
            identifier=producerIdentifier,
            isDBFetch=isDBFetch,
        )

    @staticmethod
    def getProducers(signal):
        signalId = signal
        return Producer.objects.filter(signal=signalId)

    def genPublishAttrs(self):
        return {
            "exchange": self.getModelQS().route.exchange.name,
            "routing_key": self.getModelQS().route.routing_key,
            "properties": self.getModelQS().properties,
        }

    def exec(self, msg):
        rabbitMQ = RabbitMQ()
        if rabbitMQ.isMQMQEnabled():
            rabbitMQ.publish(self.genPublishAttrs(), msg)
        return {"detail": "success"}
