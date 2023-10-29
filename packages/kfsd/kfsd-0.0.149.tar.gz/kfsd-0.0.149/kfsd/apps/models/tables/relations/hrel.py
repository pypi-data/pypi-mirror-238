from django.db import models

from kfsd.apps.models.tables.base import BaseModel
from kfsd.apps.models.constants import MAX_LENGTH


class HRel(BaseModel):
    type = models.CharField(max_length=MAX_LENGTH)

    class Meta:
        app_label = "models"
        verbose_name = "HRel"
        verbose_name_plural = "HRels"
