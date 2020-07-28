import unittest
#from unittest import mock
#from unittest.mock import patch
#from unittest.mock import MagicMock
from deconzpy import Sensor


class SensorElementTest(unittest.TestCase):

	def test_Sensor_init(self):
		#pass
		#mock = MagicMock(return_value=None)
		#with patch('deconzpy.Sensor.Light._Light__setSate', mock):
		di = dict()
		di['name'] = "TestSensor"
		di['type'] = "ZHASwitch"
		l = Sensor.Sensor(0, di, 'base/URL') # just create a trash obj
		self.assertEqual(l.getName(),"TestSensor") #make sure values of dict are there
		self.assertEqual(l.getIcon(),"🕹") #make sure values of dict are there