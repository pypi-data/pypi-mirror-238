from rest_framework import serializers

from kfsd.apps.endpoints.serializers.relations.hierarchy import (
    ChildrenViewSerializer,
    ParentViewSerializer,
)
from kfsd.apps.endpoints.serializers.relations.base import BaseHRelModelSerializer
from kfsd.apps.models.tables.general.reference import Reference


class ReferenceModelSerializer(BaseHRelModelSerializer):
    attrs = serializers.JSONField(default=dict)

    class Meta:
        model = Reference
        fields = "__all__"


class ReferenceViewModelSerializer(ReferenceModelSerializer):
    id = None
    created = None
    updated = None
    relations_from = None
    hierarchy_init = None
    children = ChildrenViewSerializer(many=True, read_only=True)
    parents = ParentViewSerializer(many=True, read_only=True)

    class Meta:
        model = Reference
        exclude = ("created", "updated", "id")
