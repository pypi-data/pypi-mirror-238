from rest_framework import serializers

from kfsd.apps.endpoints.serializers.relations.relation import (
    RelationViewModelSerializer,
)
from kfsd.apps.endpoints.serializers.relations.hierarchy import (
    HierarchyInitModelSerializer,
    HierarchyModelSerializer,
    ChildrenViewSerializer,
    ParentViewSerializer,
)

from kfsd.apps.endpoints.serializers.model import BaseModelSerializer


class BaseHRelModelSerializer(BaseModelSerializer):
    identifier = serializers.CharField()
    type = serializers.CharField()
    relations = RelationViewModelSerializer(many=True, read_only=True)
    relations_from = RelationViewModelSerializer(many=True, read_only=True)
    hierarchy_init = HierarchyInitModelSerializer(many=True, read_only=True)
    children = HierarchyModelSerializer(many=True, read_only=True)
    parents = HierarchyModelSerializer(many=True, read_only=True)


class BaseHRelViewModelSerializer(BaseHRelModelSerializer):
    id = None
    created = None
    updated = None
    relations_from = None
    hierarchy_init = None
    children = ChildrenViewSerializer(many=True, read_only=True)
    parents = ParentViewSerializer(many=True, read_only=True)
