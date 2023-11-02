from django.db import models

from kfsd.apps.core.utils.system import System
from kfsd.apps.models.constants import MAX_LENGTH
from kfsd.apps.models.tables.base import BaseModel
from kfsd.apps.models.tables.general.source import Source


def gen_media_id(sourceId, mediaId):
    if sourceId:
        return "{},MEDIA_ID={}".format(sourceId, mediaId)
    else:
        return "MEDIA_ID={}".format(mediaId)


# Github, Twitter, Linkedin, Youtube, Website
class Media(BaseModel):
    link = models.TextField()
    source = models.ForeignKey(Source, on_delete=models.CASCADE, null=True, blank=True)
    media_id = models.CharField(max_length=MAX_LENGTH)

    def save(self, *args, **kwargs):
        self.media_id = System.api_key(6)
        if self.source:
            self.identifier = gen_media_id(self.source.identifier, self.media_id)
        else:
            self.identifier = gen_media_id(None, self.media_id)
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "Media"
        verbose_name_plural = "Media"
