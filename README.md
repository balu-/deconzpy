# deconzpy
[![Build Status](https://travis-ci.org/balu-/deconzpy.svg?branch=master)](https://travis-ci.org/balu-/deconzpy)
[![Coverage Status](https://coveralls.io/repos/github/balu-/deconzpy/badge.svg?branch=master)](https://coveralls.io/github/balu-/deconzpy?branch=master)

Homeautomation Library for the tech savvy (depending on zigbee/deconz-rest)

__This should be a library to easily build home automation scripts on top of the deconz-rest api__
It can be used to easily issue comands to devices connected to deconz, subscribe to events and mix the two.
For example: on motion -> switch light on

### Sample Code

```python
from deconzpy import Router
router = Router() # Router is a singelton, can be called in multiple places and will return the same Router Object
##
# print some objects
##
sensors = router.getAllSensors()
for s in sensors:
    s.println()
print("---")
lights = router.getAllLights()
for l in lights:
    l.println()

# subscribe to websocket (for updates)
router.startAndRunThread()

#get motion sensors
bewegungsmelder = router.getSensorsByIcon("🏃‍♂️")

def onMotion(sensor, key_that_changed, oldval, newval):
	print("somebody moved - or stoped moving")

bewegungsmelder[0].subscribeToAttribute("state_presence", onMotion)
```
