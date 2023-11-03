from django.db import models
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    RegexValidator,
)

from kfsd.apps.models.tables.base import BaseModel
from kfsd.apps.models.constants import MAX_LENGTH, MIN_LENGTH
from kfsd.apps.models.constants import TYPE_REGEX_CONDITION


def gen_hierarchy_id(parentId, childId):
    return ",".join(
        [
            "PARENT={}".format(parentId),
            "CHILD={}".format(childId),
        ]
    )


class BaseHierarchy(BaseModel):
    class Meta:
        abstract = True

    parent_type = models.CharField(
        max_length=MAX_LENGTH,
        validators=[
            RegexValidator(
                regex=TYPE_REGEX_CONDITION,
                message="parent_type doesnt match condition {}".format(
                    TYPE_REGEX_CONDITION
                ),
            ),
            MaxLengthValidator(MAX_LENGTH),
            MinLengthValidator(MIN_LENGTH),
        ],
    )
    child_type = models.CharField(
        max_length=MAX_LENGTH,
        validators=[
            RegexValidator(
                regex=TYPE_REGEX_CONDITION,
                message="child_type doesnt match condition {}".format(
                    TYPE_REGEX_CONDITION
                ),
            ),
            MaxLengthValidator(MAX_LENGTH),
            MinLengthValidator(MIN_LENGTH),
        ],
    )

    def save(self, *args, **kwargs):
        self.identifier = gen_hierarchy_id(
            self.parent.identifier, self.child.identifier
        )
        return super().save(*args, **kwargs)


class HierarchyInit(BaseHierarchy):
    parent = models.ForeignKey(
        "HRel", on_delete=models.DO_NOTHING, related_name="hierarchy_init"
    )
    child = models.ForeignKey("HRel", on_delete=models.DO_NOTHING)

    class Meta:
        app_label = "models"
        verbose_name = "HierarchyInit"
        verbose_name_plural = "HierarchiesInit"


class Hierarchy(BaseHierarchy):
    parent = models.ForeignKey(
        "HRel", on_delete=models.CASCADE, related_name="children"
    )
    child = models.ForeignKey("HRel", on_delete=models.CASCADE, related_name="parents")

    class Meta:
        app_label = "models"
        verbose_name = "Hierarchy"
        verbose_name_plural = "Hierarchies"
