import re
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from django.http import Http404
from rest_framework.exceptions import ValidationError

from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.models.constants import OPERATION_ADD
from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.relations.hrel import (
    HRelModelSerializer,
    HRelViewModelSerializer,
)

from kfsd.apps.models.tables.relations.hierarchy import Hierarchy, HierarchyInit
from kfsd.apps.models.tables.relations.hrel import HRel
from kfsd.apps.endpoints.handlers.relations.hierarchy_init import rm_all_hierarchies
from kfsd.apps.endpoints.handlers.relations.relation import rm_all_relations


def gen_hrel_handler(instance):
    handler = HRelHandler(instance.identifier, False)
    qsData = HRelModelSerializer(instance=instance)
    handler.setModelQSRawData(qsData)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


def handle_pre_delete_process(instance):
    rm_all_hierarchies(instance)
    rm_all_relations(instance)


@receiver(post_save, sender=HRel)
def process_post_save(sender, instance, created, **kwargs):
    pass


@receiver(post_delete, sender=HRel)
def process_post_del(sender, instance, **kwargs):
    pass


@receiver(pre_delete, sender=HRel)
def process_pre_del(sender, instance, **kwargs):
    handle_pre_delete_process(instance)


class HRelHandler(BaseHandler):
    HIERARCHY_INIT = "hierarchy_init"
    CHILDREN = "children"
    PARENTS = "parents"
    CHILD = "child"
    PARENT = "parent"

    def __init__(self, hrelIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=HRelModelSerializer,
            viewSerializer=HRelViewModelSerializer,
            modelClass=HRel,
            identifier=hrelIdentifier,
            isDBFetch=isDBFetch,
        )

    def getHierarchyInit(self):
        return DictUtils.get(self.getModelQSData(), self.HIERARCHY_INIT)

    def getChildren(self):
        return DictUtils.get(self.getModelQSData(), self.CHILDREN)

    def getParents(self):
        return DictUtils.get(self.getModelQSData(), self.PARENTS)

    def getRelationQS(self, relationTbl, parentQS, childQS):
        return relationTbl.objects.filter(parent=parentQS, child=childQS)

    def createRelation(self, relationTbl, **kwargs):
        relationTbl.objects.create(**kwargs)

    def removeRelation(self, relationQS):
        relationQS.delete()

    def clearRelations(self, relationTbl):
        entriesQS = relationTbl.objects.filter(parent=self.getModelQS())
        entriesQS.delete()

    def upsertRelation(self, relationTbl, targetQS, operation):
        fieldChanged = False
        relationQS = self.getRelationQS(relationTbl, self.getModelQS(), targetQS)
        if operation == OPERATION_ADD:
            if not relationQS:
                self.createRelation(
                    relationTbl,
                    parent=self.getModelQS(),
                    child=targetQS,
                    parent_type=self.getModelQS().type,
                    child_type=targetQS.type,
                )
                fieldChanged = True
        else:
            if not relationQS:
                raise Http404
            self.removeRelation(relationQS)
            fieldChanged = True
        return fieldChanged

    def getUniqIdentifierRegex(self):
        # extend later
        return None

    def applyUniqIdentifierRegex(self, identifier):
        regex = self.getUniqIdentifierRegex()
        if regex:
            return re.sub(regex, "", identifier)
        return identifier

    def getParentIdentifiers(self):
        parents = self.getParents()
        parentIds = []
        for parentData in parents:
            parentId = parentData[self.PARENT]
            parentIds.append(self.applyUniqIdentifierRegex(parentId))
        return parentIds

    def isValidHierarchyInitRelation(self, targetQS, operation):
        if self.applyUniqIdentifierRegex(
            self.getIdentifier()
        ) == self.applyUniqIdentifierRegex(targetQS.identifier):
            raise ValidationError(
                "Circular depedency error, cannot add hierarchy to the same object: {}".format(
                    self.getIdentifier()
                )
            )

        if (
            operation == OPERATION_ADD
            and self.applyUniqIdentifierRegex(targetQS.identifier)
            in self.getParentIdentifiers()
        ):
            raise ValidationError(
                "Circular dependency error, obj: {} uses obj: {}".format(
                    self.getIdentifier(), targetQS.identifier
                )
            )

    def upsertHierarchyInit(self, targetQS, operation):
        self.isValidHierarchyInitRelation(targetQS, operation)
        fieldChanged = self.upsertRelation(HierarchyInit, targetQS, operation)
        return {"detail": fieldChanged}

    def populateChildren(self, store):
        childIdentifiers = [child[self.CHILD] for child in store]
        childIdentifiersQS = self.getIdentifiersQS(childIdentifiers)
        for targetQS in childIdentifiersQS:
            self.upsertRelation(Hierarchy, targetQS, OPERATION_ADD)

    def generateChildren(self, store):
        hierarchyInitData = self.getHierarchyInit()
        for hierarchy in hierarchyInitData:
            childDataHandler = HRelHandler(hierarchy[self.CHILD], True)
            store += childDataHandler.getChildren()
            store.append(hierarchy)

    def updateParentsChildren(self):
        parents = self.getParentIdentifiers()
        for parentIdentifier in parents:
            if self.getIdentifier() != parentIdentifier:
                parentHandler = HRelHandler(parentIdentifier, True)
                parentHandler.refreshHierarchy()

    def refreshHierarchy(self):
        self.clearRelations(Hierarchy)
        self.refreshModelQSData()
        store = []
        self.generateChildren(store)
        self.populateChildren(store)
        self.refreshModelQSData()
        self.updateParentsChildren()
