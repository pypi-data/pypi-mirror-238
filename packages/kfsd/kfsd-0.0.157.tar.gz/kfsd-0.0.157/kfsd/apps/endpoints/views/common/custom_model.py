from kfsd.apps.endpoints.views.common.model import ModelViewSet
from rest_framework.response import Response
from rest_framework import status


class CustomModelViewSet(ModelViewSet):
    lookup_field = "identifier"
    lookup_value_regex = "[^/]+"

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
