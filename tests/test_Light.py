import unittest
from unittest import mock
from unittest.mock import patch
from unittest.mock import MagicMock
from deconzpy import Light


class LightElementTest(unittest.TestCase):

	def test_Light_init(self):
		#pass
		mock = MagicMock(return_value=None)
		with patch('deconzpy.Light.Light._Light__setSate', mock):
			di = dict()
			di['state'] =dict()
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
			l.revokeState(10)
			self.assertFalse(l.hasState(10)) #make sure state 10 is there





if __name__ == '__main__':
    unittest.main(warnings='ignore')