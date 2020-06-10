#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sched
from threading import Thread
import traceback
import time
import websocket
from .Light import Light
from .Group import Group
from .Sensor import Sensor
from .Rule import Rule
from .Config import Config
import requests
import json

import logging
logger = logging.getLogger(__name__)


class _Singleton(type):
    """ A metaclass that creates a Singleton base class when called. """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(_Singleton("SingletonMeta", (object,), {})):
    """ Singelton Class"""
    pass


class RouterConfig(Config):
    """
        Config for the Router,
        mainly just ip of deconz and api token / username
    """

    def __init__(self, file):
        Config.__init__(
            self,
            file,
            defaultConfig={
                "gatewayIP": "1.1.1.1",
                "username": "user"})

    def getApiUrl(self, path):
        return ("http://" + self.get("gatewayIP") + "/api/" + self.get("username") + "/" + path)


# imports for ws
# import _thread
# debugging
# for websocket thread
# import _thread
# for scheduler

# from threading import Thread


class Router(Singleton):
    """ Router

        The heart and entrypoint of the lib,
        a Singleton so the router exists only once but might be accessed from multiple places

        Reads its config from "config.json"

        (!Note to get and process update values from deconz the function "startAndRunThread" needs to be calld once,
        this might be changed in the future so that its no longer needed)

    """

    def __init__(self):
        logger.debug("ROUTER: INIT")
        self.__config = RouterConfig("config.json")
        self.__groups = []
        self.__loadAllGroups()
        self.__sensors = []
        self.__loadAllSensors()
        self.__rules = []
        self.__loadAllRules()
        self.__lights = []
        self.__loadAllLights()
        self._t = None # Thread for websocket

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
            logger.warning("Could not find obj %s", key)
            return None

    def getSensorsByName(self, key):
        el = [x for x in self.__sensors if x.getName() == key]
        if el:
            return el
        else:
            # maybe lazyload
            logger.warning("Could not find obj %s", key)
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
            logger.warning("Could not find obj %s", key)
            return None

    def getRule(self, key):
        el = [x for x in self.__rules if x.getId() == key]
        if el:
            return el[0]
        else:
            # maybe lazyload
            logger.warning("Could not find obj %s", key)
            return None

    def getAllLights(self):
        return self.__lights

    def getLight(self, key):
        el = [x for x in self.__lights if x.getId() == key]
        if el:
            return el[0]
        else:
            # maybe lazyload
            logger.warning("Could not find obj %s", key)
            return None

    def getLightByName(self, key):
        el = [x for x in self.__lights if x.getName() == key]
        if el:
            return el[0]
        else:
            # maybe lazyload
            logger.warning("Could not find obj %s", key)
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
            logger.warning("Could not find obj %s", urlArray[0])
            return None

    # schaltet alles aus und räumt den stack auf
    def setOff(self):
        alleLights = self.getAllLights()
        for light in alleLights:
            if (light.getType() != "Window covering device"
                and light.isReachable()):  # do not switch off curtains
                light.actionOff()

    def __processChange(self, url, state):
        obj = self.getRessourceFromUrl(url)
        if obj is not None:
            obj.update(state)
        else:
            logger.warning("obj not found, could not update state")

    def __ws_on_message(self, message):
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
                    logger.warning("dont know what to do")
                    logger.warning(obj)

            # color
            color = objId % 7
            printString = "\x1b[1;3" + str(color + 1) + ";40m"

            url = "/" + obj["r"] + "/" + obj["id"] + "/"
            eventTranslate = {"changed": "♻️  - "}
            msg = ""
            if obj["e"] in eventTranslate:
                msg += eventTranslate[obj["e"]]
            else:
                msg += "❔" + obj["e"] + "-"
            msg += url  # lookupAddress(url)
            printString += msg
            if "state" in obj:
                printString += "   " + str(obj["state"])
            else:
                printString += "   " + str(obj)
            printString += "\x1b[0m"
            logger.info(printString)
        except Exception as error:
            logger.error(type(error).__name__)
            logger.error("Obj: %s", str(obj))
            logger.error(traceback.format_exc())
            logger.exception(error)

    def __ws_on_error(self, error):
        logger.error("### error ###")
        logger.error(error)

    def __ws_on_close(self):
        logger.info("### closed ###")

    def __ws_on_open(self):
        logger.info("### opened ###")
        logger.info(str(self))
        # print(str(ws))

    def _ws_thread_entry(self):
        logger.info("## THREAD RUNNING ##")
        websocket.enableTrace(False)
        # websocket.enableTrace(True)
        wso = websocket.WebSocketApp(
            "ws://" + self.__config.get("gatewayIP") + ":443",
            on_message=self.__ws_on_message,
            on_error=self.__ws_on_error,
            on_close=self.__ws_on_close,
        )
        wso.on_open = self.__ws_on_open
        logger.info("## WS RUN forever ")
        while True:  # try reconnect when disconnected
            try:
                wso.run_forever()
            except BaseException:
                logger.info("Websocket error - reconnect ")
                time.sleep(30)  # don't be agressive in reconnecting

    def startAndRunThread(self):
        """ Start and Run Websocket listener
           -> processes updates & state changes to the objects living in the router """
        logger.info("start & run thread")
        self._t = Thread(target=self._ws_thread_entry, args=())
        self._t.daemon = True
        self._t.start()
        # _thread.start_new_thread( self._ws_thread_entry, ("Thread-1", 2, ) )
        # _thread.start_new_thread( self._ws_thread_entry, tuple() )
        # scheduler
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.__schedulerThread = Thread(
            target=self.__runScheduler, args=(self.scheduler,)
        )
        self.__schedulerThread.daemon = True
        self.__schedulerThread.start()

    def __runScheduler(self, sched):
        maxSleep = 3
        while True:
            # print("Scheduling thread")
            try:
                wTime = sched.run(blocking=False)
            except Exception as e:
                logger.error("Exception in shedule event: %s", e)
                logger.exception(e)
            if wTime is None or wTime > maxSleep:
                wTime = maxSleep
            time.sleep(wTime)
