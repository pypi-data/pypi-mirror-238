from django.db import models

from kfsd.apps.models.constants import MAX_LENGTH
from kfsd.apps.models.tables.base import BaseModel
from kfsd.apps.models.tables.rabbitmq.route import Route
from kfsd.apps.models.tables.signals.signal import Signal
from kfsd.apps.core.utils.system import System


def gen_producer_id(uniqId):
    return uniqId


class Producer(BaseModel):
    signal = models.ForeignKey(
        Signal, on_delete=models.CASCADE, related_name="producers"
    )
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    properties = models.JSONField(default=dict)
    uniq_id = models.CharField(max_length=MAX_LENGTH)

    def save(self, *args, **kwargs):
        if not self.identifier:
            self.uniq_id = System.uuid(32)
            self.identifier = gen_producer_id(self.uniq_id)
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "Producer"
        verbose_name_plural = "Producers"
