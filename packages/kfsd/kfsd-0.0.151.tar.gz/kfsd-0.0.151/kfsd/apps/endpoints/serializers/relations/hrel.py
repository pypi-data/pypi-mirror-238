from kfsd.apps.endpoints.serializers.relations.base import (
    BaseHRelModelSerializer,
    BaseHRelViewModelSerializer,
)
from kfsd.apps.models.tables.relations.hrel import HRel


class HRelModelSerializer(BaseHRelModelSerializer):
    class Meta:
        model = HRel
        fields = "__all__"


class HRelViewModelSerializer(BaseHRelViewModelSerializer):
    class Meta:
        model = HRel
        exclude = ("created", "updated", "id")
