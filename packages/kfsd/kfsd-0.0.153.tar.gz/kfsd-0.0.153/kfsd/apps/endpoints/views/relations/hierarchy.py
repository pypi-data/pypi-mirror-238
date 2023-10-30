from drf_spectacular.utils import extend_schema_view

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.relations.hierarchy import Hierarchy
from kfsd.apps.endpoints.serializers.relations.hierarchy import (
    HierarchyModelSerializer,
)
from kfsd.apps.endpoints.views.relations.docs.hierarchy import HierarchyDoc


@extend_schema_view(**HierarchyDoc.modelviewset())
class HierarchyModelViewSet(CustomModelViewSet):
    queryset = Hierarchy.objects.all()
    serializer_class = HierarchyModelSerializer
