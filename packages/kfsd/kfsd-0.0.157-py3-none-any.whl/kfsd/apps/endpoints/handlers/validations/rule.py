from functools import reduce
import operator

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError

from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.validations.rule import (
    RuleModelSerializer,
    RuleViewModelSerializer,
)

from kfsd.apps.models.tables.validations.rule import Rule

from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.utils.attr import AttrUtils
from kfsd.apps.core.utils.arr import ArrUtils
from kfsd.apps.core.common.logger import Logger, LogLevel

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


def gen_rule_handler(instance):
    handler = RuleHandler(instance.identifier, False)
    qsData = RuleModelSerializer(instance=instance)
    handler.setModelQSRawData(qsData)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


@receiver(post_save, sender=Rule)
def process_post_save(sender, instance, created, **kwargs):
    pass


@receiver(post_delete, sender=Rule)
def process_post_del(sender, instance, **kwargs):
    pass


def intersection(arr1, arr2):
    if ArrUtils.intersection(arr1, arr2):
        return True
    return False


def filter_relations(obj, **input):
    relationKeys = ["name", "value", "source", "target"]
    if not isinstance(obj, AttrUtils):
        raise ValidationError("obj expected to be 'request' of either user or resource")

    isRevRelation = False
    if "rev" in input:
        if input["rev"] is True:
            isRevRelation = True

    relations = getattr(obj, "relations_from" if isRevRelation else "relations")
    matchingRelationKeysDict = DictUtils.filter_by_keys(input, relationKeys)

    if "field" not in input:
        raise ValidationError("'field' argument not passed")
    field = input["field"]

    matchingValues = []
    for relation in relations:
        allValesMatched = True
        for k, v in matchingRelationKeysDict.items():
            if not isinstance(v, list):
                v = [v]
            if not getattr(relation, k, None) in v:
                allValesMatched = False
        if allValesMatched:
            matchingValues.append(getattr(relation, field))

    return matchingValues


def filter_hierarchies(obj, **input):
    onValues = ["parents", "children"]
    parentsKeys = ["parent", "parent_type"]
    childrenKeys = ["child", "child_type"]

    if not isinstance(obj, AttrUtils):
        raise ValidationError("obj expected to be 'request' of either user or resource")

    if "on" not in input or DictUtils.get(input, "on") not in onValues:
        raise ValidationError(
            "'on' input expected with possible values in {}".format(onValues)
        )

    on = input.pop("on")
    matchingHierarchyKeysDict = DictUtils.filter_by_keys(
        input, parentsKeys if on == "parents" else childrenKeys
    )
    if "field" not in input:
        raise ValidationError("'field' argument not passed")
    field = input["field"]

    matchingValues = []
    for hierarchy in getattr(obj, on):
        allValuesMatched = True
        for k, v in matchingHierarchyKeysDict.items():
            if not isinstance(v, list):
                v = [v]
            if not getattr(hierarchy, k, None) in v:
                allValuesMatched = False

        if allValuesMatched:
            matchingValues.append(getattr(hierarchy, field))

    return matchingValues


class RuleHandler(BaseHandler):
    EXPR = "expr"
    ALLOF = "allOf"
    ANYOF = "anyOf"
    VAR = "var"
    CTX = "ctx"
    KEYPATH = "keypath"
    VALUES = "values"
    IS_SUCCESS = "is_success"
    DEBUG = "debug"
    DATA = "data"
    TRACE = "trace"
    ERRORS = "errors"

    def __init__(self, ruleIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=RuleModelSerializer,
            viewSerializer=RuleViewModelSerializer,
            modelClass=Rule,
            identifier=ruleIdentifier,
            isDBFetch=isDBFetch,
        )
        self.__errors = []
        self.__traces = {}
        self.__isSuccess = False

    def getExpr(self):
        return DictUtils.get(self.getModelQSData(), self.EXPR)

    def getAllOf(self):
        return DictUtils.get(self.getModelQSData(), self.ALLOF)

    def getAnyOf(self):
        return DictUtils.get(self.getModelQSData(), self.ANYOF)

    def getName(self):
        return DictUtils.get(self.getModelQSData(), "name")

    def getType(self):
        return DictUtils.get(self.getModelQSData(), "type")

    def getPrefetch(self):
        return DictUtils.get(self.getModelQSData(), "prefetch", [])

    def setRaw(self, data):
        self.__raw = data

    def getRaw(self):
        return self.__raw

    def getErrors(self):
        return self.__errors

    def getTraces(self):
        return self.__traces

    def processRuleByType(self, rule):
        if self.EXPR in rule and DictUtils.get(rule, self.EXPR):
            return self.ruleExpr(DictUtils.get(rule, self.EXPR))
        elif self.ALLOF in rule and DictUtils.get(rule, self.ALLOF):
            return self.ruleAllOf(DictUtils.get(rule, self.ALLOF))
        elif self.ANYOF in rule and DictUtils.get(rule, self.ANYOF):
            return self.ruleAnyOf(DictUtils.get(rule, self.ANYOF))
        return False

    def ruleAnyOf(self, anyOf):
        return reduce(operator.or_, (self.processRuleByType(rule) for rule in anyOf))

    def ruleAllOf(self, allOf):
        return reduce(operator.and_, (self.processRuleByType(rule) for rule in allOf))

    def ruleExpr(self, expr, default=False):
        result = default
        request = AttrUtils.format_dict(self.__raw)  # noqa: F841
        input = self.__raw  # noqa: F841
        try:
            result = eval(expr)
        except Exception as e:
            extnError = ""
            if isinstance(e, KeyError):
                extnError = "not found"
            self.__errors.append(
                "exception while executing expr: '{}', error: {} {}".format(
                    expr, e.args[0], extnError
                )
            )
        self.__traces[expr] = result
        return result

    def getValues(self):
        rule = self.getModelQSData()
        return DictUtils.get(rule, self.VALUES)

    def evaluate(self):
        rule = self.getModelQSData()
        if DictUtils.get(rule, self.VALUES) and self.processRuleByType(rule):
            self.__isSuccess = True

    def genCtx(self, step):
        var = DictUtils.get(step, self.VAR)
        val = self.processRuleByType(step)
        return var, val

    def genCtxAll(self):
        for value in self.getPrefetch():
            var, val = self.genCtx(value)
            self.__raw[self.CTX] = DictUtils.merge(
                dict1=DictUtils.get(self.__raw, self.CTX, {}), dict2={var: val}
            )

    def summarize(self):
        return {
            self.IS_SUCCESS: self.__isSuccess,
            self.VALUES: self.getValues(),
            self.DEBUG: {
                # self.DATA: self.__raw,
                self.ERRORS: self.__errors,
                self.TRACE: self.__traces,
            },
        }

    def exec(self, data):
        self.setRaw(data)
        self.genCtxAll()
        self.evaluate()
