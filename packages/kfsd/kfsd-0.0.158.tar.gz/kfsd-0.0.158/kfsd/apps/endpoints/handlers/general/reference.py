from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.handlers.signals.outbound import upsert_tbl_event

from kfsd.apps.models.tables.general.reference import Reference
from kfsd.apps.endpoints.serializers.general.reference import (
    ReferenceModelSerializer,
    ReferenceViewModelSerializer,
)


def gen_reference_handler(instance):
    handler = ReferenceHandler(instance.identifier, False)
    qsData = ReferenceModelSerializer(instance=instance)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


@receiver(post_save, sender=Reference)
@upsert_tbl_event(gen_reference_handler)
def process_post_save(sender, instance, created, **kwargs):
    pass


@receiver(post_delete, sender=Reference)
@upsert_tbl_event(gen_reference_handler)
def process_post_del(sender, instance, **kwargs):
    pass


class ReferenceHandler(BaseHandler):
    def __init__(self, referenceIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=ReferenceModelSerializer,
            viewSerializer=ReferenceViewModelSerializer,
            modelClass=Reference,
            identifier=referenceIdentifier,
            isDBFetch=isDBFetch,
        )
