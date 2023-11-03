from django.db import models
from django.utils.text import slugify

from kfsd.apps.models.constants import MAX_LENGTH
from kfsd.apps.models.tables.base import BaseModel


def gen_source_id(type, name):
    return "TYPE={},SOURCE={}".format(type, name)


# Github, Twitter, Linkedin, Youtube, Website
class Source(BaseModel):
    name = models.CharField(max_length=MAX_LENGTH)
    type = models.CharField(max_length=MAX_LENGTH)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.identifier = gen_source_id(self.type, self.name)
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "Source"
        verbose_name_plural = "Sources"
