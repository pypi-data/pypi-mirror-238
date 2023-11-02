from django.db import models

from kfsd.apps.models.tables.base import BaseModel
from kfsd.apps.models.constants import MAX_LENGTH
from kfsd.apps.models.tables.general.data import Data

RULE_MAX_LENGTH = 400


def gen_policy_id(type, name):
    return "POLICY_TYPE={},POLICY_NAME={}".format(type, name)


class Policy(BaseModel):
    name = models.CharField(max_length=MAX_LENGTH)
    type = models.CharField(max_length=MAX_LENGTH)
    resources = models.ManyToManyField(Data)
    all_values = models.JSONField(default=list)

    def save(self, *args, **kwargs):
        self.identifier = gen_policy_id(self.name, self.type)
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "Policy"
        verbose_name_plural = "Policies"
