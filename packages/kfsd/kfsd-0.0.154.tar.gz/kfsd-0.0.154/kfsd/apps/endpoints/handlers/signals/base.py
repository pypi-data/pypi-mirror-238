from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.handlers.validations.policy import PolicyHandler
from kfsd.apps.endpoints.handlers.signals.signal import SignalHandler

from kfsd.apps.core.common.logger import Logger, LogLevel
from kfsd.apps.core.utils.system import System
from kfsd.apps.core.utils.dict import DictUtils

from kfsd.apps.models.tables.signals.base import log_error
from kfsd.apps.models.tables.signals.signal import gen_signal_id

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class BaseSignalHandler(BaseHandler):
    ENV_POLICY_ID = "env_policy_id"

    def __init__(self, **kwargs):
        self.__envPolicyId = DictUtils.get(kwargs, self.ENV_POLICY_ID)
        BaseHandler.__init__(self, **kwargs)
        self.__isRetain = False

    def getPolicyIdFromEnv(self):
        return System.getEnv(self.__envPolicyId)

    def getData(self):
        return DictUtils.get(self.getModelQSData(), "data")

    def getPolicyHandler(self):
        return PolicyHandler(self.getPolicyIdFromEnv(), True)

    def getSignals(self):
        policyHandler = self.getPolicyHandler()
        policyHandler.exec(self.getData())
        signals = policyHandler.getEvaluatedValues()
        if not signals:
            logger.warn(
                "[POLICY][{}]No signals found for data: {} ...SKIPPED!".format(
                    policyHandler.getIdentifier(), self.getData()
                )
            )
            return []
        return [SignalHandler(gen_signal_id(signal), True) for signal in signals]

    def delete(self):
        if not self.__isRetain:
            self.getModelQS().delete()

    def execSignals(self):
        signalHandlers = self.getSignals()
        for signalHandler in signalHandlers:
            signalHandler.exec(self.getData())
            if signalHandler.isRetain():
                self.__isRetain = True

    def exec(self):
        try:
            self.execSignals()
            self.delete()
        except Exception as e:
            logger.error(
                "Recd error in processing signal: {}, error: {}".format(
                    e, self.getData()
                )
            )
            log_error(self.getModelQS(), e.__str__())
