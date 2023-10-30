from django.db import models

from kfsd.apps.models.tables.base import BaseModel
from kfsd.apps.models.constants import MAX_LENGTH
from kfsd.apps.models.tables.validations.policy import Policy

RULE_MAX_LENGTH = 400


def gen_rule_id(policyId, name):
    return "{},RULE={}".format(policyId, name)


class Rule(BaseModel):
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name="rules")
    name = models.CharField(max_length=MAX_LENGTH)
    prefetch = models.JSONField(default=list)
    values = models.JSONField(default=list)
    expr = models.CharField(max_length=RULE_MAX_LENGTH)
    anyOf = models.JSONField(default=list)
    allOf = models.JSONField(default=list)

    def save(self, *args, **kwargs):
        self.identifier = gen_rule_id(self.policy.identifier, self.name)
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "Rule"
        verbose_name_plural = "Rule"
