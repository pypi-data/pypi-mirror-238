from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.relations.hierarchy import (
    HierarchyModelSerializer,
)

from kfsd.apps.models.tables.relations.hierarchy import Hierarchy


def gen_hierarchy_handler(instance):
    handler = HierarchyHandler(instance.identifier, False)
    qsData = HierarchyModelSerializer(instance=instance)
    handler.setModelQSRawData(qsData)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


@receiver(post_save, sender=Hierarchy)
def process_post_save(sender, instance, created, **kwargs):
    pass


@receiver(post_delete, sender=Hierarchy)
def process_post_del(sender, instance, **kwargs):
    pass


class HierarchyHandler(BaseHandler):
    def __init__(self, hierarchyIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=HierarchyModelSerializer,
            viewSerializer=HierarchyModelSerializer,
            modelClass=Hierarchy,
            identifier=hierarchyIdentifier,
            isDBFetch=isDBFetch,
        )
