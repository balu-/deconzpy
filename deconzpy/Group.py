#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from .BaseElement import DeconzBaseElement


class Scene(DeconzBaseElement):
    def __init__(self, id, arr, urlRoot):
        DeconzBaseElement.__init__(self, id, arr, urlRoot)

    def getName(self):
        return self.getAttribute("name")

    def println(self):
        print(self.getId() + " " + self.getName() + " - " + self.getUrlRoot())

    def recall(self):
        # /<scene_id>/recall
        r = requests.put(self.getUrlRoot() + "/" + self.getId() + "/recall")


class Group(DeconzBaseElement):
    """ Repraesentation einer Gruppe """

    def __init__(self, id, arr, urlRoot):
        DeconzBaseElement.__init__(self, id, arr, urlRoot)
        self.__scenes = []
        if self.getAttribute("scenes"):  # create Scene array
            for sce in self.getAttribute("scenes"):
                self.__scenes.append(
                    Scene(
                        sce["id"],
                        sce,
                        self.getUrlRoot() + "/" + self.getId() + "/scenes",
                    )
                )

    def getName(self):
        return self.getAttribute("name")

    def getScenes(self):
        return self.__scenes

    def getSceneByName(self, name):
        el = [x for x in self.__scenes if x.getName() == name]
        if el:
            return el[0]
        else:
            return None

    def actionOn(self):
        r = requests.put(
            self.getUrlRoot() + "/" + self.getId() + "/action", json={"on": True}
        )
        # print(r.status_code)
        # print(r.text)

    def actionOff(self):
        r = requests.put(
            self.getUrlRoot() + "/" + self.getId() + "/action", json={"on": False}
        )

    def actionAlert(self):
        # PUT /api/<apikey>/groups/<id>/action
        pass  # { 'action': 'lselect' }

    def println(self):
        print(
            self.getId() + " " + self.getName() + " - S:" + str(len(self.getScenes()))
        )
