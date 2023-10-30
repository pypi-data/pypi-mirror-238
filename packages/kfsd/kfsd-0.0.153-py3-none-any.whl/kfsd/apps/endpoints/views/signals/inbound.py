from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import renderers

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.signals.inbound import Inbound
from kfsd.apps.endpoints.serializers.signals.inbound import InboundViewModelSerializer
from kfsd.apps.endpoints.views.signals.docs.inbound import InboundDoc
from kfsd.apps.endpoints.handlers.signals.inbound import InboundHandler


@extend_schema_view(**InboundDoc.modelviewset())
class InboundModelViewSet(CustomModelViewSet):
    queryset = Inbound.objects.all()
    serializer_class = InboundViewModelSerializer

    @extend_schema(**InboundDoc.clear_view())
    @action(detail=False, methods=["get"], renderer_classes=[renderers.JSONRenderer])
    def clear(self, request, identifier=None):
        return Response(InboundHandler.clear())
