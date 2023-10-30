from kfsd.apps.models.tables.signals.base import BaseSignal


def gen_outbound_id(uniqId):
    return uniqId


class Outbound(BaseSignal):
    class Meta:
        app_label = "models"
        verbose_name = "Outbound"
        verbose_name_plural = "Outbound"
