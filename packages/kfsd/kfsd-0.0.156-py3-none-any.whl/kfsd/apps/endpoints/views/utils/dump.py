from rest_framework import viewsets, decorators, response, status
from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.utils.docs.dump import DumpDoc
from kfsd.apps.endpoints.renderers.kubefacetsjson import KubefacetsJSONRenderer
from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.common.logger import Logger, LogLevel

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class DumpViewSet(viewsets.ViewSet):
    lookup_field = "identifier"
    serializer_class = None

    def parseInput(self, request):
        input = {
            "method": request.method,
            "path": request.path,
            "content_type": request.content_type,
            "query_params": request.query_params,
            "headers": DictUtils.filter_by_keys_neg(request.headers, ["Cache-Control"]),
            "body": request.data,
            "cookies": request.COOKIES,
        }
        logger.info("Recd content (Dump API): {}".format(input))
        return input

    @extend_schema(**DumpDoc.dump_get_view())
    @decorators.action(
        detail=False, methods=["get"], renderer_classes=[KubefacetsJSONRenderer]
    )
    def get(self, request):
        return response.Response(self.parseInput(request), status.HTTP_200_OK)

    @extend_schema(**DumpDoc.dump_post_view())
    @decorators.action(
        detail=False, methods=["post"], renderer_classes=[KubefacetsJSONRenderer]
    )
    def post(self, request):
        return response.Response(self.parseInput(request), status.HTTP_200_OK)

    @extend_schema(**DumpDoc.dump_put_view())
    @decorators.action(
        detail=False, methods=["put"], renderer_classes=[KubefacetsJSONRenderer]
    )
    def put(self, request):
        return response.Response(self.parseInput(request), status.HTTP_200_OK)

    @extend_schema(**DumpDoc.dump_delete_view())
    @decorators.action(
        detail=False, methods=["delete"], renderer_classes=[KubefacetsJSONRenderer]
    )
    def delete(self, request):
        return response.Response(self.parseInput(request), status.HTTP_200_OK)

    @extend_schema(**DumpDoc.dump_patch_view())
    @decorators.action(
        detail=False, methods=["patch"], renderer_classes=[KubefacetsJSONRenderer]
    )
    def patch(self, request):
        return response.Response(self.parseInput(request), status.HTTP_200_OK)
