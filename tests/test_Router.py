import unittest
from unittest import mock
from unittest.mock import patch
from unittest.mock import MagicMock
from deconzpy import Router


class RouterElementTest(unittest.TestCase):

	def getRouter(self,mock=None):
		if mock == None:
			mock = MagicMock(return_value=None)
		with patch('deconzpy.Router._Router__loadAllSensors', mock):
			with patch('deconzpy.Router._Router__loadAllRules', mock):
				with patch('deconzpy.Router._Router__loadAllLights', mock):
					with patch('deconzpy.Router._Router__loadAllGroups', mock):
						#seems to hard to mock or i'm not bright enough
						r = Router()
						return r


	def test_Router_init(self):
		#pass
		r = self.getRouter()
		r2 = self.getRouter()
		self.assertEqual(r, r2) #Router is a sigleton and should be the same object always

	def test_Router_getAllGroups(self):
		r = self.getRouter()
		self.assertEqual(r.getAllGroups(), []) #elementlists should be empty

	def test_Router_getAllSensors(self):
		r = self.getRouter()
		self.assertEqual(r.getAllSensors(), []) #elementlists should be empty

	def test_Router_getAllLights(self):
		r = self.getRouter()
		self.assertEqual(r.getAllLights(), []) #elementlists should be empty





if __name__ == '__main__':
    unittest.main(warnings='ignore')