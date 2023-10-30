from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.rabbitmq.queue import (
    QueueModelSerializer,
    QueueViewModelSerializer,
)
from kfsd.apps.models.tables.rabbitmq.queue import Queue


def gen_queue_handler(instance):
    handler = QueueHandler(instance.identifier, False)
    qsData = QueueModelSerializer(instance=instance)
    handler.setModelQSRawData(qsData)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


@receiver(post_save, sender=Queue)
def process_post_save(sender, instance, created, **kwargs):
    pass


@receiver(post_delete, sender=Queue)
def process_post_del(sender, instance, **kwargs):
    pass


class QueueHandler(BaseHandler):
    def __init__(self, queueIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=QueueModelSerializer,
            viewSerializer=QueueViewModelSerializer,
            modelClass=Queue,
            identifier=queueIdentifier,
            isDBFetch=isDBFetch,
        )
