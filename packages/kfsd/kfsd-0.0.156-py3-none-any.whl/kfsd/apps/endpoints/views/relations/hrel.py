from drf_spectacular.utils import extend_schema_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.relations.hrel import HRel
from kfsd.apps.endpoints.handlers.relations.hrel import HRelHandler
from kfsd.apps.endpoints.serializers.relations.hrel import (
    HRelViewModelSerializer,
)
from kfsd.apps.endpoints.views.relations.docs.hrel import HRelDoc, HRelHierarchyDoc
from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.models.constants import OPERATION_ADD, OPERATION_DELETE


@extend_schema_view(**HRelDoc.modelviewset())
class HRelModelViewSet(CustomModelViewSet):
    queryset = HRel.objects.all()
    serializer_class = HRelViewModelSerializer


@extend_schema_view(**HRelHierarchyDoc.modelviewset())
class HRelHierarchyViewSet(APIView):
    renderer_classes = [JSONRenderer]
    serializer_class = None

    def validateUserInputs(self, kwargs):
        parentIdentifier = DictUtils.get(kwargs, "parent")
        childIdentifier = DictUtils.get(kwargs, "child")
        missingIdentifiers = []
        if not HRelHandler(parentIdentifier, False).exists():
            missingIdentifiers.append(
                "Identifier: {} not found".format(parentIdentifier)
            )

        if not HRelHandler(childIdentifier, False).exists():
            missingIdentifiers.append(
                "Identifier: {} not found".format(childIdentifier)
            )

        if missingIdentifiers:
            raise ValidationError(missingIdentifiers)

        parentHandler = HRelHandler(parentIdentifier, True)
        childHandler = HRelHandler(childIdentifier, True)
        return parentHandler, childHandler

    def post(self, request, *args, **kwargs):
        parentHandler, childHandler = self.validateUserInputs(kwargs)
        respData = parentHandler.upsertHierarchyInit(
            childHandler.getModelQS(), OPERATION_ADD
        )
        return Response(respData, status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        parentHandler, childHandler = self.validateUserInputs(kwargs)
        respData = parentHandler.upsertHierarchyInit(
            childHandler.getModelQS(), OPERATION_DELETE
        )
        return Response(respData, status.HTTP_200_OK)
