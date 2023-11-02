from django.db import models

from kfsd.apps.models.tables.relations.hrel import HRel


class Reference(HRel):
    attrs = models.JSONField(default=dict)

    class Meta:
        app_label = "models"
        verbose_name = "Reference"
        verbose_name_plural = "References"
