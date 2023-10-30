from django.db import models

from kfsd.apps.models.tables.base import BaseModel
from kfsd.apps.models.tables.rabbitmq.route import Route
from kfsd.apps.models.tables.signals.signal import Signal


def gen_producer_id(routeId):
    return routeId


class Producer(BaseModel):
    signals = models.ManyToManyField(Signal, related_name="producers")
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    properties = models.JSONField(default=dict)

    def save(self, *args, **kwargs):
        self.identifier = gen_producer_id(self.route.identifier)
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "Producer"
        verbose_name_plural = "Producers"
