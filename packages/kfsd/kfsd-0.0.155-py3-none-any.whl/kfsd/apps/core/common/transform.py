from kfsd.apps.core.utils.dict import DictUtils


class Transform:
    KEYPATH = "keypath"
    VALUE = "value"

    def __init__(self, rules, data):
        self.__rules = rules
        self.__data = data

    def exec(self):
        for rule in self.__rules:
            keys = rule[self.KEYPATH].split(".")
            val = rule[self.VALUE]
            newValDict = DictUtils.create_hierarchy(keys, val)
            self.__data = DictUtils.merge(dict1=self.__data, dict2=newValDict)
        return self.__data
