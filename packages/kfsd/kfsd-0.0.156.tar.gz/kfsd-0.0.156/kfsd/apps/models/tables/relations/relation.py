from django.db import models
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    RegexValidator,
)

from kfsd.apps.models.constants import (
    RELATION_NAME_REGEX_CONDITION,
    TYPE_REGEX_CONDITION,
    MAX_LENGTH,
    MIN_LENGTH,
)
from kfsd.apps.models.tables.base import BaseModel


def gen_relation_id(name, sourceId, targetId):
    identifierData = [
        "NAME={}".format(name),
        "SOURCE={}".format(sourceId),
        "TARGET={}".format(targetId),
    ]
    return ",".join(identifierData)


class Relation(BaseModel):
    name = models.CharField(
        max_length=MAX_LENGTH,
        validators=[
            RegexValidator(
                regex=RELATION_NAME_REGEX_CONDITION,
                message="name doesnt match condition {}".format(
                    RELATION_NAME_REGEX_CONDITION
                ),
            ),
            MaxLengthValidator(MAX_LENGTH),
            MinLengthValidator(MIN_LENGTH),
        ],
    )
    value = models.CharField(
        max_length=MAX_LENGTH,
        validators=[
            RegexValidator(
                regex=TYPE_REGEX_CONDITION,
                message="relation value doesnt match condition {}".format(
                    TYPE_REGEX_CONDITION
                ),
            ),
            MaxLengthValidator(MAX_LENGTH),
            MinLengthValidator(MIN_LENGTH),
        ],
    )
    source = models.ForeignKey(
        "HRel", on_delete=models.DO_NOTHING, related_name="relations"
    )
    target = models.ForeignKey(
        "HRel", on_delete=models.DO_NOTHING, related_name="relations_from"
    )

    def save(self, *args, **kwargs):
        self.identifier = gen_relation_id(
            self.name, self.source.identifier, self.target.identifier
        )
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "Relation"
        verbose_name_plural = "Relations"
