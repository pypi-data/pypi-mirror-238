from rest_framework import serializers

from kfsd.apps.models.tables.relations.hrel import HRel
from kfsd.apps.models.tables.relations.hierarchy import HierarchyInit, Hierarchy

from kfsd.apps.endpoints.serializers.model import BaseModelSerializer


class BaseHierarchyViewModelSerializer(BaseModelSerializer):
    id = None
    created = None
    updated = None
    slug = None
    parent = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field="identifier",
        queryset=HRel.objects.all(),
    )
    child = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field="identifier",
        queryset=HRel.objects.all(),
    )


class HierarchyInitModelSerializer(BaseHierarchyViewModelSerializer):
    class Meta:
        model = HierarchyInit
        exclude = (
            "id",
            "created",
            "updated",
        )


class HierarchyModelSerializer(BaseHierarchyViewModelSerializer):
    class Meta:
        model = Hierarchy
        exclude = (
            "id",
            "created",
            "updated",
        )


class ChildrenViewSerializer(BaseHierarchyViewModelSerializer):
    parent = None
    parent_type = None
    identifier = None

    class Meta:
        model = Hierarchy
        exclude = ("id", "created", "updated", "parent", "parent_type", "identifier")


class ParentViewSerializer(BaseHierarchyViewModelSerializer):
    child = None
    child_type = None
    identifier = None

    class Meta:
        model = Hierarchy
        exclude = ("id", "created", "updated", "child", "child_type", "identifier")
