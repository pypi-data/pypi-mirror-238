from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import renderers

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.validations.rule import Rule
from kfsd.apps.endpoints.serializers.validations.rule import RuleViewModelSerializer
from kfsd.apps.endpoints.views.validations.docs.rule import RuleDoc
from kfsd.apps.endpoints.handlers.validations.rule import RuleHandler


@extend_schema_view(**RuleDoc.modelviewset())
class RuleModelViewSet(CustomModelViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleViewModelSerializer

    @extend_schema(**RuleDoc.exec_view())
    @action(
        detail=True,
        methods=["post"],
        renderer_classes=[renderers.JSONRenderer, renderers.StaticHTMLRenderer],
    )
    def exec(self, request, identifier=None):
        ruleHandler = RuleHandler(identifier, True)
        ruleHandler.exec(request.data)
        return Response(ruleHandler.summarize())
