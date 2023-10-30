from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.requests.template import (
    RequestTemplateModelSerializer,
    RequestTemplateViewModelSerializer,
)

from kfsd.apps.models.tables.requests.template import RequestTemplate


def gen_request_template_handler(instance):
    handler = RequestTemplateHandler(instance.identifier, False)
    qsData = RequestTemplateModelSerializer(instance=instance)
    handler.setModelQSRawData(qsData)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


@receiver(post_save, sender=RequestTemplate)
def process_post_save(sender, instance, created, **kwargs):
    pass


@receiver(post_delete, sender=RequestTemplate)
def process_post_del(sender, instance, **kwargs):
    pass


class RequestTemplateHandler(BaseHandler):
    def __init__(self, templateIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=RequestTemplateModelSerializer,
            viewSerializer=RequestTemplateViewModelSerializer,
            modelClass=RequestTemplate,
            identifier=templateIdentifier,
            isDBFetch=isDBFetch,
        )

    def getHeaders(self):
        return self.getModelQS().headers.all()

    def getParams(self):
        return self.getModelQS().params.all()
