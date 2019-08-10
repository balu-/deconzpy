class BaseElement:
    def __init__(self, id, arr):
        arr = self.__flatDict(arr)
        self.__val = arr
        self.__id = id
        self.__subs = {}  # dict {'attribute':[ function-pointer ]}
        self.__subsAllwaysCall = (
            {}
        )  # dict {'attribute':[ function-pointer ]} # subscribers that want to be called even if value did not change

    def getId(self):
        return self.__id

    def println(self):
        print(self.getId())

    def __flatDict(self, obj, preKey=""):
        """ 
		convertiert ein dict mit verschiedenen unter dicts
		in ein dict der tiefe 1
		keys werden prependet: aus { "test" : { "test" : "value" }}
							  wird { "test_test" : "value" }
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
        obj = self.__flatDict(obj)
        updatedValues = {}
        # obj is an object with values
        for key, value in obj.items():
            if not key in self.__val:  # init key if not existing
                self.__val[key] = ""
            if self.__val[key] != value:  # check for new value
                updatedValues[key] = self.__val[key]  # save old value
                self.__val[key] = value
        # call all subscribers on updated Values
        for attributeName, value in updatedValues.items():
            if attributeName in self.__subs:
                for func in self.__subs[attributeName]:
                    func(
                        self, attributeName, value, self.__val[attributeName]
                    )  # obj, key, oldval, newval
        # call all subscribers that want to be called weather or not value did change
        for attributeName, value in obj.items():
            if attributeName in self.__subsAllwaysCall:
                for func in self.__subsAllwaysCall[attributeName]:
                    # get oldvalue if availiable
                    oldvalue = value
                    if attributeName in updatedValues:
                        oldvalue = updatedValues[attributeName]
                    func(self, attributeName, oldvalue, self.__val[attributeName])

    def subscribeToAttribute(self, attributeName, func, callOnlyIfValueChanged=True):
        if not callOnlyIfValueChanged:  # subscribe to subsallwayscall
            if not attributeName in self.__subsAllwaysCall:
                self.__subsAllwaysCall[attributeName] = []
            if not func in self.__subsAllwaysCall[attributeName]:
                self.__subsAllwaysCall[attributeName].append(func)
        else:  # subscribe to subs
            if not attributeName in self.__subs:
                self.__subs[attributeName] = []
            if not func in self.__subs[attributeName]:
                self.__subs[attributeName].append(func)

    def unsubscribeFromAttribute(self, attributeName, func):
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
        if key in self.__val:
            return self.__val[key]
        else:
            return None

    def dump(self):
        print(self.getId() + " - " + str(self.__val))


class DeconzBaseElement(BaseElement):
    def __init__(self, id, arr, urlRoot):
        self.__urlRoot = urlRoot
        BaseElement.__init__(self, id, arr)

    def getUrlRoot(self):
        return self.__urlRoot


# Test
if __name__ == "__main__":
    b1 = BaseElement(1, {"test": {"tut": {"tat": "tit"}}})
    if b1.getAttribute("test_tut_tat") != "tit":
        print("Test fehlgeschlagen")
    else:
        print("Test erfolgreich")
