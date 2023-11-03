from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.signals.signal import (
    SignalModelSerializer,
    SignalViewModelSerializer,
)
from kfsd.apps.endpoints.handlers.rabbitmq.producer import ProducerHandler
from kfsd.apps.endpoints.handlers.signals.webhook import WebhookHandler
from kfsd.apps.endpoints.handlers.validations.policy import gen_policy_handler

from kfsd.apps.models.tables.signals.signal import Signal

from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.common.transform import Transform
from kfsd.apps.core.common.logger import Logger, LogLevel

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


def gen_signal_handler(instance):
    handler = SignalHandler(instance.identifier, False)
    qsData = SignalModelSerializer(instance=instance)
    handler.setModelQSRawData(qsData)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


@receiver(post_save, sender=Signal)
def process_post_save(sender, instance, created, **kwargs):
    pass


@receiver(post_delete, sender=Signal)
def process_post_del(sender, instance, **kwargs):
    pass


class SignalHandler(BaseHandler):
    def __init__(self, signalIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=SignalModelSerializer,
            viewSerializer=SignalViewModelSerializer,
            modelClass=Signal,
            identifier=signalIdentifier,
            isDBFetch=isDBFetch,
        )

    def getName(self):
        return DictUtils.get(self.getModelQSData(), "name")

    def getProducers(self):
        return DictUtils.get(self.getModelQSData(), "producers")

    def getWebhooks(self):
        return DictUtils.get(self.getModelQSData(), "webhooks")

    def getDeliveryMethod(self):
        return DictUtils.get(self.getModelQSData(), "delivery")

    def isRetain(self):
        return DictUtils.get(self.getModelQSData(), "is_retain")

    def getTranformId(self):
        return DictUtils.get(self.getModelQSData(), "transform")

    def getTransformHandler(self):
        if self.getTranformId():
            return gen_policy_handler(self.getModelQS().transform)
        return None

    def sendMsgToProducer(self, producerId, msg):
        producerHandler = ProducerHandler(producerId, True)
        producerHandler.exec(msg)
        logger.debug(
            "[SENDING][PRODUCER][{}] {}".format(producerHandler.getIdentifier(), msg)
        )

    def sendMsgToWebhook(self, webhookId, msg):
        webhookHandler = WebhookHandler(webhookId, True)
        logger.debug(
            "[SENDING][WEBHOOK][{}] {}".format(webhookHandler.getIdentifier(), msg)
        )
        webhookHandler.exec(msg)

    def sendToAllProducers(self, msg):
        producers = self.getProducers()
        for producer in producers:
            producerId = producer["identifier"]
            self.sendMsgToProducer(producerId, msg)

    def sendToAllWebhooks(self, msg):
        webhooks = self.getWebhooks()
        for webhook in webhooks:
            webhookId = webhook["identifier"]
            self.sendMsgToWebhook(webhookId, msg)

    def exec(self, msg):
        transformHandler = self.getTransformHandler()
        if transformHandler:
            transformHandler.exec(msg)
            transform = Transform(transformHandler.getEvaluatedValues(), msg)
            msg = transform.exec()

        deliveryMethod = self.getDeliveryMethod()
        if deliveryMethod == "MSMQ":
            self.sendToAllProducers(msg)
        elif deliveryMethod == "WEBHOOK":
            self.sendToAllWebhooks(msg)
        elif deliveryMethod == "ALL":
            self.sendToAllProducers(msg)
            self.sendToAllWebhooks(msg)
        return {"detail": "success"}
