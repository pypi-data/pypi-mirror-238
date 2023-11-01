from drf_spectacular.utils import extend_schema_view

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.relations.relation import Relation
from kfsd.apps.endpoints.serializers.relations.relation import (
    RelationViewModelSerializer,
)
from kfsd.apps.endpoints.views.relations.docs.relation import RelationDoc


@extend_schema_view(**RelationDoc.modelviewset())
class RelationModelViewSet(CustomModelViewSet):
    queryset = Relation.objects.all().order_by("id")
    serializer_class = RelationViewModelSerializer
