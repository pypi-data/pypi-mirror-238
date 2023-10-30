import json

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from kfsd.apps.endpoints.handlers.general.file import gen_file_handler
from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.general.data import (
    DataModelSerializer,
    DataViewModelSerializer,
)

from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.common.template import Template

from kfsd.apps.models.constants import JSON, FILE
from kfsd.apps.models.tables.general.data import Data
from kfsd.apps.core.common.logger import Logger, LogLevel

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


def gen_data_handler(instance):
    handler = DataHandler(instance.identifier, False)
    qsData = DataModelSerializer(instance=instance)
    handler.setModelQSRawData(qsData)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


@receiver(post_save, sender=Data)
def process_post_save(sender, instance, created, **kwargs):
    pass


@receiver(post_delete, sender=Data)
def process_post_del(sender, instance, **kwargs):
    pass


class DataHandler(BaseHandler):
    def __init__(self, dataIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=DataModelSerializer,
            viewSerializer=DataViewModelSerializer,
            modelClass=Data,
            identifier=dataIdentifier,
            isDBFetch=isDBFetch,
        )

    def isTemplate(self):
        return DictUtils.get(self.getModelQSData(), "is_template")

    def getSlug(self):
        return DictUtils.get(self.getModelQSData(), "slug")

    def isFileSource(self):
        sourceType = DictUtils.get(self.getModelQSData(), "source_type")
        if sourceType == FILE:
            return True
        return False

    def isRawSource(self):
        sourceType = DictUtils.get(self.getModelQSData(), "source_type")
        if sourceType == "RAW":
            return True
        return False

    def isEndpointSource(self):
        sourceType = DictUtils.get(self.getModelQSData(), "source_type")
        if sourceType == "ENDPOINT":
            return True
        return False

    def getDefaultTemplateAttrs(self):
        return DictUtils.get(self.getModelQSData(), "default_template_values")

    def isJson(self):
        contentType = DictUtils.get(self.getModelQSData(), "content_type")
        if contentType == JSON:
            return True
        return False

    def getFileContent(self):
        if not self.getModelQS().file:
            return None

        fileHandler = gen_file_handler(self.getModelQS().file)
        return fileHandler.getFile().decode("utf-8")

    def getRawBody(self):
        return DictUtils.get(self.getModelQSData(), "raw_body")

    def getRawJsonBody(self):
        return DictUtils.get(self.getModelQSData(), "raw_json_body")

    def getEndpointResp(self, context):
        from kfsd.apps.endpoints.handlers.requests.endpoint import gen_endpoint_handler

        endpointHandler = gen_endpoint_handler(self.getModelQS().endpoint)
        return endpointHandler.exec(context)

    def genTemplate(self, body, context):
        template = Template(
            body,
            context,
            {},
            False,
            self.getDefaultTemplateAttrs(),
        )
        return template.mergeValues()

    def genBody(self, context):
        body = None
        if self.isRawSource():
            body = self.getRawBody()
            if self.isJson():
                body = self.getRawJsonBody()
        elif self.isFileSource():
            body = self.getFileContent()
            if self.isJson():
                body = json.loads(body)
        elif self.isEndpointSource():
            resp = self.getEndpointResp(context)
            if self.isJson():
                body = resp.json()
        if self.isTemplate():
            return self.genTemplate(body, context)
        return body
