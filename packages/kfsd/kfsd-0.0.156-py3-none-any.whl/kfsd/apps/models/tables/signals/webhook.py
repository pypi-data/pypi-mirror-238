from django.db import models

from kfsd.apps.models.tables.base import BaseModel
from kfsd.apps.models.tables.signals.signal import Signal
from kfsd.apps.models.tables.requests.endpoint import Endpoint


def gen_webhook_id(endpointId):
    return endpointId


class Webhook(BaseModel):
    signals = models.ManyToManyField(Signal, related_name="webhooks")
    endpoint = models.ForeignKey(Endpoint, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        self.identifier = gen_webhook_id(self.endpoint.identifier)
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "Webhook"
        verbose_name_plural = "Webhooks"
