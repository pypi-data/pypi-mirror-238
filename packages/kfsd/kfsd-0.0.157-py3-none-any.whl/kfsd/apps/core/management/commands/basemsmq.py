from django.core.management.base import BaseCommand
from kfsd.apps.core.msmq.rabbitmq.base import RabbitMQ
from kfsd.apps.core.utils.time import Time

from kfsd.apps.core.common.logger import Logger, LogLevel
from kfsd.apps.endpoints.handlers.signals.inbound import add_inbound_signal

import json

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


def base_callback(ch, method, properties, body):
    bodyStr = body.decode().replace("'", '"')
    body = json.loads(bodyStr)
    add_inbound_signal(body)


class Command(BaseCommand):
    help = "Listens to a RabbitMQ topic"

    def __init__(self, callbackFn=base_callback):
        self.__callbackFn = callbackFn

    def add_arguments(self, parser):
        parser.add_argument(
            "-s",
            "--service_config_id",
            type=str,
            help="Service Config Id",
        )

    def connectToMSMQ(self):
        try:
            msmqHandler = RabbitMQ.getSingleton()
            return msmqHandler
        except Exception as e:
            print(e)
            logger.error(
                "Error connecting to RabbitMQ, check if RabbitMQ instance is up!"
            )
            Time.sleep(30)
            self.connectToMSMQ()

    def handle(self, *args, **options):
        logger.info("Listening to MSMQ messages...")
        msmqHandler = self.connectToMSMQ()
        if msmqHandler.isMQMQEnabled():
            msmqHandler.consumeQueues(self.__callbackFn)
            msmqHandler.startConsuming()
        else:
            logger.info("MSMQ is disabled")
