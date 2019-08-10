#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

class _Singleton(type):
    """ A metaclass that creates a Singleton base class when called. """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(_Singleton("SingletonMeta", (object,), {})):
    pass


from .Config import Config


class RouterConfig(Config):
    # config
    def __init__(self, file):
        Config.__init__(
            self, file, defaultConfig={"gatewayIP": "1.1.1.1", "username": "user"}
        )

    def getApiUrl(self, path):
        return (
            "http://"
            + self.get("gatewayIP")
            + "/api/"
            + self.get("username")
            + "/"
            + path
        )


from .Rule import Rule

from .Sensor import Sensor

from .Group import Group

from .Light import Light

# imports for ws
import websocket

# import _thread
import time

# debugging
import traceback

# for websocket thread
# import _thread
# for scheduler
import sched, time
from threading import Thread

# from threading import Thread


class Router(Singleton):
    def __init__(self):
        print("ROUTER: INIT")
        self.__config = RouterConfig("config.json")
        self.__groups = []
        self.__loadAllGroups()
        self.__sensors = []
        self.__loadAllSensors()
        self.__rules = []
        self.__loadAllRules()
        self.__lights = []
        self.__loadAllLights()

    def getAllGroups(self):
        return self.__groups

    def getGroupByName(self, name):
        el = [x for x in self.__groups if x.getName() == name]
        if el:
            return el[0]
        else:
            return None

    def getAllRules(self):
        return self.__rules

    def getAllSensors(self):
        return self.__sensors

    def getSensor(self, key):
        el = [x for x in self.__sensors if x.getId() == key]
        if el:
            return el[0]
        else:
            # maybe lazyload
            print("Could not find obj " + key)
            return None

    def getSensorsByName(self, key):
        el = [x for x in self.__sensors if x.getName() == key]
        if el:
            return el
        else:
            # maybe lazyload
            print("Could not find obj " + key)
            return None

    def getSensorsByIcon(self, icon):
        el = [x for x in self.__sensors if x.getIcon() == icon]
        return el

    def getGroup(self, key):
        el = [x for x in self.__groups if x.getId() == key]
        if el:
            return el[0]
        else:
            # maybe lazyload
            print("Could not find obj " + key)
            return None

    def getRule(self, key):
        el = [x for x in self.__rules if x.getId() == key]
        if el:
            return el[0]
        else:
            # maybe lazyload
            print("Could not find obj " + key)
            return None

    def getAllLights(self):
        return self.__lights

    def getLight(self, key):
        el = [x for x in self.__lights if x.getId() == key]
        if el:
            return el[0]
        else:
            # maybe lazyload
            print("Could not find obj " + key)
            return None

    def getLightByName(self, key):
        el = [x for x in self.__lights if x.getName() == key]
        if el:
            return el[0]
        else:
            # maybe lazyload
            print("Could not find obj " + key)
            return None

    def __loadAllGroups(self):
        r = requests.get(self.__config.getApiUrl("groups"), timeout=3)
        obj = r.json()
        ret = []
        for id, r in obj.items():
            # get detailed group
            ret.append(Group(id, r, self.__config.getApiUrl("groups")))
        self.__groups = sorted(ret, key=lambda tup: int(tup.getId()))
        # print(json.dumps(r.json(), indent=4, sort_keys=True))

    def __loadAllSensors(self):
        """Request Sensors via api, returns Array of Sensor objects (sorted)"""
        r = requests.get(self.__config.getApiUrl("sensors"), timeout=3)
        obj = r.json()
        ret = []
        for i, val in obj.items():
            ret.append(Sensor(i, val, self.__config.getApiUrl("sensors")))
        self.__sensors = sorted(ret, key=lambda tup: int(tup.getId()))

    def __loadAllRules(self):
        r = requests.get(self.__config.getApiUrl("rules"), timeout=3)
        obj = r.json()
        ret = []
        for i, r in obj.items():
            ret.append(Rule(i, r, self.__config.getApiUrl("rules")))
        self.__rules = sorted(ret, key=lambda tup: int(tup.getId()))
        # print(json.dumps(r.json(), indent=4, sort_keys=True))

    def __loadAllLights(self):
        r = requests.get(self.__config.getApiUrl("lights"), timeout=3)
        obj = r.json()
        ret = []
        for i, r in obj.items():
            ret.append(Light(i, r, self.__config.getApiUrl("lights")))
        self.__lights = sorted(ret, key=lambda tup: int(tup.getId()))
        # print(json.dumps(r.json(), indent=4, sort_keys=True))

    def getRessourceFromUrl(self, url):
        urlArray = url.split("/")
        if urlArray[0] == "sensors":
            return self.getSensor(urlArray[1])
        elif urlArray[0] == "groups":
            return self.getGroup(urlArray[1])
        elif urlArray[0] == "lights":
            return self.getLight(urlArray[1])
        elif urlArray[0] == "rules":
            return self.getRule(urlArray[1])
        else:
            print("Could not find obj " + urlArray[0])
            return None

    # schaltet alles aus und räumt den stack auf
    def setOff(self):
        alleLights = self.getAllLights()
        for light in alleLights:
            if (
                light.getType() != "Window covering device"
            ):  # do not switch off curtains
                light.actionOff()

    def __processChange(self, url, state):
        obj = self.getRessourceFromUrl(url)
        if obj != None:
            obj.update(state)
        else:
            print("obj not found, could not update state")

    def __ws_on_message(self, ws, message):
        # print(message)
        try:
            obj = json.loads(message)
            objId = int(obj["id"])

            if obj["e"] == "changed":
                # process change
                url = "" + obj["r"] + "/" + obj["id"] + "/"
                if "state" in obj:
                    self.__processChange(url, {"state": obj["state"]})
                # guesswork
                elif "config" in obj:
                    self.__processChange(url, {"config": obj["config"]})
                else:
                    print("dont know what to do")
                    print(obj)

            # color
            color = objId % 7
            print("\x1b[1;3" + str(color + 1) + ";40m", end="")

            url = "/" + obj["r"] + "/" + obj["id"] + "/"
            eventTranslate = {"changed": "♻️  - "}
            msg = ""
            if obj["e"] in eventTranslate:
                msg += eventTranslate[obj["e"]]
            else:
                msg += "❔" + obj["e"] + "-"
            msg += url  # lookupAddress(url)
            print(msg)
            if "state" in obj:
                print("   " + str(obj["state"]))
            else:
                print("   " + str(obj))
            print("\x1b[0m", end="")
        except Exception as error:
            print(type(error).__name__)
            print(error)
            print("Obj: ", end="")
            print(obj)
            traceback.print_exc()

    def __ws_on_error(self, ws, error):
        print("### error ###")
        print(error)

    def __ws_on_close(self, ws):
        print("### closed ###")

    def __ws_on_open(self, ws):
        print("### opened ###")

    def _ws_thread_entry(self):
        print("## THREAD RUNNING ##")
        websocket.enableTrace(False)
        wso = websocket.WebSocketApp(
            "ws://" + self.__config.get("gatewayIP") + ":443",
            on_message=self.__ws_on_message,
            on_error=self.__ws_on_error,
            on_close=self.__ws_on_close,
        )
        wso.on_open = self.__ws_on_open
        wso.run_forever()

    def startAndRunThread(self):
        print("start & run thread")
        self.__t = Thread(target=self._ws_thread_entry, args=())
        self.__t.start()
        # _thread.start_new_thread( self._ws_thread_entry, ("Thread-1", 2, ) )
        # _thread.start_new_thread( self._ws_thread_entry, tuple() )
        # scheduler
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.__schedulerThread = Thread(
            target=self.__runScheduler, args=(self.scheduler,)
        )
        self.__schedulerThread.start()

    def __runScheduler(self, sched):
        maxSleep = 3
        while True:
            # print("Scheduling thread")
            wTime = sched.run(blocking=False)
            if wTime == None or wTime > maxSleep:
                wTime = maxSleep
            time.sleep(wTime)
