#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .BaseElement import DeconzBaseElement


class Rule(DeconzBaseElement):
    """ Class representing a Rule """

    class Condition:
        def __init__(self, arr, lookupAddrFunction=lambda adrStr: adrStr):
            self.__val = arr
            self.lookupAddress = lookupAddrFunction

        def getAddress(self):
            """Translate Adress"""
            return self.lookupAddress(self.__val["address"])

        def getOperator(self):
            odict = {"eq": "=", "gt": ">", "lt": "<"}
            if self.__val["operator"] in odict:
                return odict[self.__val["operator"]]
            else:
                return self.__val["operator"]

        def getValue(self):
            if "value" in self.__val:
                return self.__val["value"]
            else:
                return ""

        def println(self):
            print(self.getAddress(), self.getOperator(), self.getValue())

    class Action:
        def __init__(self, arr, lookupAddrFunction=lambda adrStr: adrStr):
            self.__val = arr
            self.lookupAddress = lookupAddrFunction

        def getAddress(self):
            # return self.__val["address"]
            return self.lookupAddress(self.__val["address"])

        def getBody(self):
            return self.__val["body"]

        def getMethod(self):
            return self.__val["method"]

        def println(self):
            ret = self.getAddress() + " - "
            ret += self.getMethod() + " - "
            ret += str(self.getBody())
            print(ret)

    def __init__(self, id, arr, urlRoot, lookupAddrFunction=lambda adrStr: adrStr):
        DeconzBaseElement.__init__(self, id, arr, urlRoot)
        self.lookupAddress = lookupAddrFunction
        self.__conditions = []
        self.__actions = []
        for c in arr["conditions"]:
            self.__conditions.append(Rule.Condition(c, self.lookupAddress))
        for a in arr["actions"]:
            self.__actions.append(Rule.Action(a, self.lookupAddress))

    def getName(self):
        return self.getAttribute("name")

    def getActions(self):
        # return self.__val['actions']
        return self.__actions

    def getConditions(self):
        # return self.__val['conditions']
        return self.__conditions

    def println(self):
        color = int(self.getId()) % 7
        print(
            "\x1b[1;3"
            + str(color + 1)
            + ";40m"
            + "{:2d} : ".format(int(self.getId()))
            + "{:30.30s}".format(self.getName())
        )
        for c in self.getConditions():
            print("   + ", end="")
            c.println()
        print("   =>")
        for a in self.getActions():
            print("    > ", end="")
            a.println()
        print("" + "\x1b[0m")
