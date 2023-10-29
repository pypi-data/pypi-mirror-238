import json
import urllib.parse

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.requests.endpoint import (
    EndpointModelSerializer,
    EndpointViewModelSerializer,
)
from kfsd.apps.endpoints.handlers.requests.template import gen_request_template_handler

from kfsd.apps.models.tables.requests.endpoint import Endpoint

from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.utils.http.base import HTTP
from kfsd.apps.core.common.template import Template


def gen_endpoint_handler(instance):
    handler = EndpointHandler(instance.identifier, False)
    qsData = EndpointModelSerializer(instance=instance)
    handler.setModelQSRawData(qsData)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


@receiver(post_save, sender=Endpoint)
def process_post_save(sender, instance, created, **kwargs):
    pass


@receiver(post_delete, sender=Endpoint)
def process_post_del(sender, instance, **kwargs):
    pass


class EndpointHandler(BaseHandler, HTTP):
    def __init__(self, endpointIdentifier, isDBFetch):
        HTTP.__init__(self)
        BaseHandler.__init__(
            self,
            serializer=EndpointModelSerializer,
            viewSerializer=EndpointViewModelSerializer,
            modelClass=Endpoint,
            identifier=endpointIdentifier,
            isDBFetch=isDBFetch,
        )

    def getUrl(self):
        return DictUtils.get(self.getModelQSData(), "url")

    def genTemplate(self, body, context):
        template = Template(
            body,
            context,
            {},
            False,
            {},
        )
        return template.mergeValues()

    def getMethod(self):
        return DictUtils.get(self.getModelQSData(), "method")

    def getSuccessCode(self):
        return DictUtils.get(self.getModelQSData(), "success_code")

    def getRequestTemplateHandler(self):
        if not self.getModelQS().request_template:
            return None
        return gen_request_template_handler(self.getModelQS().request_template)

    def getRequestTemplateHeaders(self):
        headers = {}
        requestTemplateHandler = self.getRequestTemplateHandler()
        if not requestTemplateHandler:
            return headers
        return {
            headerInstance.key: headerInstance.value
            for headerInstance in requestTemplateHandler.getHeaders()
        }

    def getRequestTemplateParams(self):
        params = {}
        requestTemplateHandler = self.getRequestTemplateHandler()
        if not requestTemplateHandler:
            return params
        return {
            paramInstance.key: paramInstance.value
            for paramInstance in requestTemplateHandler.getParams()
        }

    def getFormattedHeaders(self):
        return {header["key"]: header["value"] for header in self.getHeaders()}

    def getReqMethod(self, method):
        methodMap = {
            "GET": HTTP().get,
            "POST": HTTP().post,
            "DELETE": HTTP().delete,
            "PATCH": HTTP().patch,
        }
        return methodMap[method]

    def getDataHandler(self):
        from kfsd.apps.endpoints.handlers.general.data import gen_data_handler

        if not self.getModelQS().body:
            return None
        return gen_data_handler(self.getModelQS().body)

    def getReqBody(self, context):
        dataHandler = self.getDataHandler()
        if dataHandler:
            return dataHandler.genBody(context)
        return ""

    def isJsonType(self, text):
        try:
            json.dumps(text)
            return True
        except Exception:
            return False

    def constructReqUrl(self, context):
        parsed_url = urllib.parse.urlparse(self.getUrl())
        existing_params = urllib.parse.parse_qs(parsed_url.query)
        existing_params.update(self.getRequestTemplateParams())
        query_params = urllib.parse.urlencode(existing_params, doseq=True)
        url = urllib.parse.urlunparse(
            (
                parsed_url.scheme,
                parsed_url.netloc,
                parsed_url.path,
                parsed_url.params,
                query_params,
                parsed_url.fragment,
            )
        )
        url = self.genTemplate(url, context)
        return url

    def exec(self, context):
        url = self.constructReqUrl(context)
        reqMethodType = self.getMethod()
        reqMethod = self.getReqMethod(reqMethodType)
        headers = self.getRequestTemplateHeaders()
        successCode = self.getSuccessCode()
        kwargs = {"headers": headers}
        reqBody = self.getReqBody(context)
        if reqBody:
            if self.isJsonType(reqBody):
                kwargs["json"] = reqBody
            else:
                kwargs["body"] = reqBody
        resp = reqMethod(url, successCode, **kwargs)
        return resp
