from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import renderers

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.signals.outbound import Outbound
from kfsd.apps.endpoints.serializers.signals.outbound import OutboundViewModelSerializer
from kfsd.apps.endpoints.views.signals.docs.outbound import OutboundDoc
from kfsd.apps.endpoints.handlers.signals.outbound import OutboundHandler


@extend_schema_view(**OutboundDoc.modelviewset())
class OutboundModelViewSet(CustomModelViewSet):
    queryset = Outbound.objects.all()
    serializer_class = OutboundViewModelSerializer

    @extend_schema(**OutboundDoc.clear_view())
    @action(detail=False, methods=["get"], renderer_classes=[renderers.JSONRenderer])
    def clear(self, request, identifier=None):
        return Response(OutboundHandler.clear())
