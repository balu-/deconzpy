#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .BaseElement import DeconzBaseElement
import requests


class Sensor(DeconzBaseElement):
    """Class representing a Sensor"""

    def __init__(self, id, arr, urlRoot):
        DeconzBaseElement.__init__(self, id, arr, urlRoot)

    def getName(self):
        return self.getAttribute("name")

    def getType(self):
        return self.getAttribute("type")

    def getIcon(self):
        idict = {
            "ZHASwitch": "🕹 ",
            "ZHALightLevel": "🌅",  # 🌗🌅
            "ZHAPresence": "🏃‍♂️",
            "CLIPPresence": "🏃‍♂️",
            "ZHATemperature": "🌡 ",
            "ZHAThermostat": "🌡 ",
            "CLIPGenericStatus": "🚥",
            "Daylight": "🌓",
            "ZHAWater": "💦",
            "ZHAOpenClose": "🚪",
        }
        if self.getType() in idict:
            return idict[self.getType()]
        else:
            return "❓"

    def getManufactur(self):
        return self.getAttribute("manufacturername")

    def setConfig(self, key, value):
        jsonObj = {key: value}
        r = requests.put(
            self.getUrlRoot() + "/" + self.getId() + "/config", json=jsonObj
        )

    def println(self):
        color = int(self.getId()) % 7
        print(
            "\x1b[1;3"
            + str(color + 1)
            + ";40m"
            + "{:2d} : ".format(int(self.getId()))
            + self.getIcon()
            + " {:7.7s} - {:30s}".format(self.getManufactur(), self.getName()),
            " - " + self.getType() + "\x1b[0m",
        )
