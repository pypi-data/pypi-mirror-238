from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.rabbitmq.route import (
    RouteModelSerializer,
    RouteViewModelSerializer,
)

from kfsd.apps.models.tables.rabbitmq.route import Route


def gen_route_handler(instance):
    handler = RouteHandler(instance.identifier, False)
    qsData = RouteModelSerializer(instance=instance)
    handler.setModelQSRawData(qsData)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


@receiver(post_save, sender=Route)
def process_post_save(sender, instance, created, **kwargs):
    pass


@receiver(post_delete, sender=Route)
def process_post_del(sender, instance, **kwargs):
    pass


class RouteHandler(BaseHandler):
    def __init__(self, routeIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=RouteModelSerializer,
            viewSerializer=RouteViewModelSerializer,
            modelClass=Route,
            identifier=routeIdentifier,
            isDBFetch=isDBFetch,
        )
