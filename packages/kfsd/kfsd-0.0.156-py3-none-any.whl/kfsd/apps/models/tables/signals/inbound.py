from kfsd.apps.models.tables.signals.base import BaseSignal


def gen_inbound_id(uniqId):
    return uniqId


class Inbound(BaseSignal):
    class Meta:
        app_label = "models"
        verbose_name = "Inbound"
        verbose_name_plural = "Inbound"
