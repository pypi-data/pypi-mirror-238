import json
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.signals.webhook import (
    WebhookModelSerializer,
    WebhookViewModelSerializer,
)
from kfsd.apps.endpoints.handlers.requests.endpoint import gen_endpoint_handler

from kfsd.apps.models.tables.signals.webhook import Webhook


def gen_webhook_handler(instance):
    handler = WebhookHandler(instance.identifier, False)
    qsData = WebhookModelSerializer(instance=instance)
    handler.setModelQSRawData(qsData)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


@receiver(post_save, sender=Webhook)
def process_post_save(sender, instance, created, **kwargs):
    pass


@receiver(post_delete, sender=Webhook)
def process_post_del(sender, instance, **kwargs):
    pass


class WebhookHandler(BaseHandler):
    def __init__(self, webhookIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=WebhookModelSerializer,
            viewSerializer=WebhookViewModelSerializer,
            modelClass=Webhook,
            identifier=webhookIdentifier,
            isDBFetch=isDBFetch,
        )

    def getEndpointHandler(self):
        return gen_endpoint_handler(self.getModelQS().endpoint)

    def exec(self, msg):
        resp = self.getEndpointHandler().exec(msg)
        if hasattr(resp, "data"):
            return resp.data
        else:
            try:
                return resp.json()
            except json.JSONDecodeError:
                return resp.content
