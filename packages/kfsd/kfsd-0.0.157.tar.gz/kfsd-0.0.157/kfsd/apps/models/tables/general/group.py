from django.db import models
from django.utils.text import slugify

from kfsd.apps.models.tables.base import BaseModel
from kfsd.apps.models.constants import MAX_LENGTH
from kfsd.apps.models.tables.general.media import Media
from kfsd.apps.models.tables.general.reference import Reference


def gen_group_id(parentId, type, name):
    id = ""
    if not parentId:
        id = ",".join(
            [
                "{}={}".format("TYPE", type.upper()),
                "{}={}".format("NAME", name),
            ]
        )
    else:
        id = ",".join(
            [
                "{}={}".format("PARENT", parentId),
                "{}={},{}".format("CHILD", type.upper(), name),
            ]
        )
    return id


class Group(BaseModel):
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True, related_name="parents"
    )
    type = models.CharField(max_length=MAX_LENGTH)
    name = models.CharField(max_length=MAX_LENGTH, unique=True)
    media = models.ManyToManyField(Media)
    members = models.ManyToManyField(Reference)
    groups = models.ManyToManyField("self", symmetrical=False)
    slug = models.SlugField()
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if not self.parent:
            self.identifier = gen_group_id(None, self.type, self.name)
        else:
            self.identifier = gen_group_id(self.parent.identifier, self.type, self.name)
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "Group"
        verbose_name_plural = "Groups"
