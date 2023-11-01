from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError

from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.relations.hierarchy import (
    HierarchyInitModelSerializer,
)

from kfsd.apps.models.tables.relations.hierarchy import HierarchyInit


def gen_hierarchy_init_handler(instance):
    handler = HierarchyInitHandler(instance.identifier, False)
    qsData = HierarchyInitModelSerializer(instance=instance)
    handler.setModelQSRawData(qsData)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


def rm_all_hierarchies(instance):
    HierarchyInit.objects.filter(parent=instance).delete()
    HierarchyInit.objects.filter(child=instance).delete()


@receiver(pre_save, sender=HierarchyInit)
def process_pre_save(sender, instance, *args, **kwargs):
    parentIdentifier = instance.parent.identifier
    childIdentifier = instance.child.identifier
    expectedIdentifier = "PARENT={},CHILD={}".format(parentIdentifier, childIdentifier)
    if instance.identifier != expectedIdentifier:
        raise ValidationError(
            "Hierarchy Identifier not as per format expected! observed: {}, expected: {}".format(
                instance.identifier, expectedIdentifier
            )
        )


@receiver(post_save, sender=HierarchyInit)
def process_post_save(sender, instance, created, **kwargs):
    from kfsd.apps.endpoints.handlers.relations.hrel import gen_hrel_handler

    hrelHandler = gen_hrel_handler(instance.parent)
    hrelHandler.refreshHierarchy()


@receiver(post_delete, sender=HierarchyInit)
def process_post_del(sender, instance, **kwargs):
    from kfsd.apps.endpoints.handlers.relations.hrel import gen_hrel_handler

    hrelHandler = gen_hrel_handler(instance.parent)
    hrelHandler.refreshHierarchy()


class HierarchyInitHandler(BaseHandler):
    def __init__(self, hierarchyInitIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=HierarchyInitModelSerializer,
            viewSerializer=HierarchyInitModelSerializer,
            modelClass=HierarchyInit,
            identifier=hierarchyInitIdentifier,
            isDBFetch=isDBFetch,
        )

    def getChildHandler(self):
        from kfsd.apps.endpoints.handlers.relations.hrel import gen_hrel_handler

        return gen_hrel_handler(self.getModelQS().child)

    def getParentHandler(self):
        from kfsd.apps.endpoints.handlers.relations.hrel import gen_hrel_handler

        return gen_hrel_handler(self.getModelQS().parent)
