from drf_spectacular.utils import extend_schema_view

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.relations.hierarchy import HierarchyInit
from kfsd.apps.endpoints.serializers.relations.hierarchy import (
    HierarchyInitModelSerializer,
)
from kfsd.apps.endpoints.views.relations.docs.hierarchy_init import HierarchyInitDoc


@extend_schema_view(**HierarchyInitDoc.modelviewset())
class HierarchyInitModelViewSet(CustomModelViewSet):
    queryset = HierarchyInit.objects.all()
    serializer_class = HierarchyInitModelSerializer
