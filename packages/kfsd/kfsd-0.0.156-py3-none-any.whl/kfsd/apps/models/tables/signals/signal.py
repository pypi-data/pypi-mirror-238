from django.db import models

from kfsd.apps.models.constants import MAX_LENGTH
from kfsd.apps.models.tables.base import BaseModel
from kfsd.apps.models.tables.validations.policy import Policy


def gen_signal_id(name):
    return "SIGNAL={}".format(name)


class Signal(BaseModel):
    name = models.CharField(max_length=MAX_LENGTH)
    delivery = models.CharField(max_length=MAX_LENGTH)
    is_retain = models.BooleanField(default=False)
    transform = models.ForeignKey(
        Policy, on_delete=models.CASCADE, blank=True, null=True
    )

    def save(self, *args, **kwargs):
        self.identifier = gen_signal_id(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "Signal"
        verbose_name_plural = "Signals"
