import unittest
from unittest import mock
from unittest.mock import patch
from unittest.mock import MagicMock
from deconzpy import Light


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LightElementTest(unittest.TestCase):

	def test_Light_init(self):
		#pass
		mock = MagicMock(return_value=None)
		with patch('deconzpy.Light.Light._Light__setSate', mock):
			di = dict()
			di['state'] = dict()
			di['state']['bri'] = 100
			l = Light.Light(0, di, 'base/URL') # just create a trash obj
			self.assertEqual(l.getBrightness(),100) #make sure values of dict are there
			self.assertTrue(l.hasState(0)) #make sure state 0 is initaly there

	def test_Light_brightness(self):
		#pass
		mock = MagicMock(return_value=None)
		with patch('deconzpy.Light.Light._Light__setSate', mock):
			di = dict()
			l = Light.Light(0, di, 'base/URL') # just create a trash obj
			
			l.setBrightness(100, statePrio=10) # set state 10
			self.assertTrue(l.hasState(10)) #make sure state 10 is there

			self.assertEqual(l.stateStack[10].brightness, 100)#check if created state has correct value

	def test_Light_actionOn(self):
		#pass
		mock = MagicMock(return_value=None)
		with patch('deconzpy.Light.Light._Light__setSate', mock):
			di = dict()
			l = Light.Light(0, di, 'base/URL') # just create a trash obj

			l.actionOn(statePrio=10, colorTemperatur=200) #set on 
			self.assertTrue(l.hasState(10)) #make sure state 10 is there
			self.assertEqual(l.stateStack[10].brightness, None)#check if created state has default (None) brightness
			self.assertEqual(l.stateStack[10].colorTemperatur, 200)#check if created state has correct value

			l.revokeState(10)
			self.assertFalse(l.hasState(10)) #make sure state 10 is there

	def test_Light_ctMax(self):
		#pass
		mock = MagicMock(return_value=None)
		with patch('deconzpy.Light.Light._Light__setSate', mock):
			di = dict()
			di['ctmax'] = 400
			l = Light.Light(0, di, 'base/URL') # just create a trash obj

			l.actionOn(statePrio=10, colorTemperatur=450) #set on 
			self.assertTrue(l.hasState(10)) #make sure state 10 is there
			self.assertEqual(l.stateStack[10].colorTemperatur, 400)#check if created state has correct value
			
			l.setColorTemperatur(350, statePrio=10)
			self.assertTrue(l.hasState(10)) #make sure state 10 is there
			self.assertEqual(l.stateStack[10].colorTemperatur, 350)#check if created state has correct value

			l.setColorTemperatur(480, statePrio=10)
			self.assertTrue(l.hasState(10)) #make sure state 10 is there
			self.assertEqual(l.stateStack[10].colorTemperatur, 400)#check if created state has correct value

			l.revokeState(10)
			self.assertFalse(l.hasState(10)) #make sure state 10 is there

	def test_Light_ctMin(self):
		#pass
		mock = MagicMock(return_value=None)
		with patch('deconzpy.Light.Light._Light__setSate', mock):
			di = dict()
			di['ctmin'] = 300
			l = Light.Light(0, di, 'base/URL') # just create a trash obj

			l.actionOn(statePrio=10, colorTemperatur=200) #set on 
			self.assertTrue(l.hasState(10)) #make sure state 10 is there
			self.assertEqual(l.stateStack[10].colorTemperatur, 300)#check if created state has correct value

			l.setColorTemperatur(350, statePrio=10)
			self.assertTrue(l.hasState(10)) #make sure state 10 is there
			self.assertEqual(l.stateStack[10].colorTemperatur, 350)#check if created state has correct value

			l.setColorTemperatur(220, statePrio=10)
			self.assertTrue(l.hasState(10)) #make sure state 10 is there
			self.assertEqual(l.stateStack[10].colorTemperatur, 300)#check if created state has correct value

			l.revokeState(10)
			self.assertFalse(l.hasState(10)) #make sure state 10 is there


	def test_Light_ctMinMax(self):
		#pass
		mock = MagicMock(return_value=None)
		with patch('deconzpy.Light.Light._Light__setSate', mock):
			di = dict()
			di['ctmin'] = 300
			di['ctmax'] = 400
			l = Light.Light(0, di, 'base/URL') # just create a trash obj

			l.actionOn(statePrio=10, colorTemperatur=350) #set on 
			self.assertTrue(l.hasState(10)) #make sure state 10 is there
			self.assertEqual(l.stateStack[10].colorTemperatur, 350)#check if created state has correct value


			l.setColorTemperatur(200, statePrio=10)
			self.assertTrue(l.hasState(10)) #make sure state 10 is there
			self.assertEqual(l.stateStack[10].colorTemperatur, 300)#check if created state has correct value

			l.setColorTemperatur(450, statePrio=10)
			self.assertTrue(l.hasState(10)) #make sure state 10 is there
			self.assertEqual(l.stateStack[10].colorTemperatur, 400)#check if created state has correct value

			l.setColorTemperatur(360, statePrio=10)
			self.assertTrue(l.hasState(10)) #make sure state 10 is there
			self.assertEqual(l.stateStack[10].colorTemperatur, 360)#check if created state has correct value

			l.revokeState(10)
			self.assertFalse(l.hasState(10)) #make sure state 10 is there






if __name__ == '__main__':
    unittest.main(warnings='ignore')