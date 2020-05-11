import logging
logger = logging.getLogger(__name__)


class BaseElement:
    """
        BaseElement

        Base Class for the Objects,
        holds the functionaly handle subscribtions to attribute changes

        params:
            id (str): object identifier
            arr (dict): dictionary of values, might be stacked (like { "key": { "key1": "value" } } )
                        internaly this dict will be converted to a dict of depth=1 (like { "key_key1": "value"})
                        [this is done to be easily able to subscribe to changes]
    """

    def __init__(self, id, arr):
        arr = self.__flatDict(arr)
        self.__val = arr
        self.__id = id
        self.__subs = {}  # dict {'attribute':[ function-pointer ]}
        # dict {'attribute':[ function-pointer ]} # subscribers that want to be
        # called even if value did not change
        self.__subsAllwaysCall = ({})

    def getId(self):
        return self.__id

    def println(self):
        """ print a representation of the element to cmd """
        print(self.getId())

    def __flatDict(self, obj, preKey=""):
        """
                converts a dict of multiple sub dicts to a dict of depth 1
                keys will be prependet: input of  { "test" : { "test" : "value" }}
                                                             will result in { "test_test" : "value" }
                """
        res = {}
        for key, value in obj.items():
            totalKey = preKey
            if totalKey != "":
                totalKey += "_"
            totalKey += key
            if isinstance(value, dict):
                value = self.__flatDict(value, preKey=totalKey)
                res.update(value)
            else:
                res[totalKey] = value
        return res

    def update(self, obj):
        """
            update attributes and call subscribed liseners to inform about the change

            Params:
                obj (dict): attributes to change
        """
        obj = self.__flatDict(obj)
        updatedValues = {}
        # obj is an object with values
        for key, value in obj.items():
            if key not in self.__val:  # init key if not existing
                self.__val[key] = ""
            if self.__val[key] != value:  # check for new value
                updatedValues[key] = self.__val[key]  # save old value
                self.__val[key] = value
        # call all subscribers on updated Values
        for attributeName, value in updatedValues.items():
            if attributeName in self.__subs:
                for func in self.__subs[attributeName]:
                    try:
                        func(
                            self, attributeName, value, self.__val[attributeName]
                        )  # obj, key, oldval, newval
                    except BaseException:
                        logger.warning("Exception in subscriber %s",str(func))
        # call all subscribers that want to be called weather or not value did
        # change
        for attributeName, value in obj.items():
            if attributeName in self.__subsAllwaysCall:
                for func in self.__subsAllwaysCall[attributeName]:
                    # get oldvalue if availiable
                    oldvalue = value
                    if attributeName in updatedValues:
                        oldvalue = updatedValues[attributeName]
                    try:
                        func(
                            self,
                            attributeName,
                            oldvalue,
                            self.__val[attributeName])
                    except BaseException:
                        logger.warning("Exception in subscriber %s", str(func))

    def subscribeToAttribute(
            self,
            attributeName,
            func,
            callOnlyIfValueChanged=True):
        """
            Add subscriber for changes to an attribute

            Param:
                attributeName (str): name of the attribute to listen for changes
                                    (!Note: this must be the 'flat_name' )
                func (function): function that should be called on change
                                (params will be: <BaseElement>, <attributeName>,<oldValue>,<newValue> )
                callOnlyIfValueChanged (Bool): call func only if newValue != oldValue
        """
        if not callOnlyIfValueChanged:  # subscribe to subsallwayscall
            if attributeName not in self.__subsAllwaysCall:
                self.__subsAllwaysCall[attributeName] = []
            if func not in self.__subsAllwaysCall[attributeName]:
                self.__subsAllwaysCall[attributeName].append(func)
        else:  # subscribe to subs
            if attributeName not in self.__subs:
                self.__subs[attributeName] = []
            if func not in self.__subs[attributeName]:
                self.__subs[attributeName].append(func)

    def unsubscribeFromAttribute(self, attributeName, func):
        """
            remove Subscriber from attribute

            Param:
                attributeName (str): name of the attribute to listen for changes
                                    (!Note: this must be the 'flat_name' )
                func (function): function that should be unsubscribed
        """
        if attributeName in self.__subs:
            try:
                self.__subs[attributeName].remove(func)
                return True
            except ValueError:
                pass  # func not in list
        elif attributeName in self.__subsAllwaysCall:
            try:
                self.__subsAllwaysCall[attributeName].remove(func)
                return True
            except ValueError:
                pass  # func not in list
        return False

    def getAttribute(self, key):
        """
            get Attribute Value for key
            Param:
                key (str): name of the attribute
                            (!Note: this must be the 'flat_name' )
        """
        if key in self.__val:
            return self.__val[key]
        else:
            return None

    def dump(self):
        print(self.getId() + " - " + str(self.__val))


class DeconzBaseElement(BaseElement):
    """
        DeconzBaseElement

        adds urlRoot to the BaseElement
        (urlRoot will be populated by the router on creation)
    """

    def __init__(self, id, arr, urlRoot):
        self.__urlRoot = urlRoot
        BaseElement.__init__(self, id, arr)

    def getUrlRoot(self):
        return self.__urlRoot
