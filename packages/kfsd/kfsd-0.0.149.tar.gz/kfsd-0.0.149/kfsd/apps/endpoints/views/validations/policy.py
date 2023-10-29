from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import renderers

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.validations.policy import Policy
from kfsd.apps.endpoints.serializers.validations.policy import PolicyViewModelSerializer
from kfsd.apps.endpoints.views.validations.docs.policy import PolicyDoc
from kfsd.apps.endpoints.handlers.validations.policy import PolicyHandler


@extend_schema_view(**PolicyDoc.modelviewset())
class PolicyModelViewSet(CustomModelViewSet):
    queryset = Policy.objects.all()
    serializer_class = PolicyViewModelSerializer

    @extend_schema(**PolicyDoc.exec_view())
    @action(
        detail=True,
        methods=["post"],
        renderer_classes=[renderers.JSONRenderer, renderers.StaticHTMLRenderer],
    )
    def exec(self, request, identifier=None):
        policyHandler = PolicyHandler(identifier, True)
        policyHandler.exec(request.data)
        return Response(policyHandler.summarize())
