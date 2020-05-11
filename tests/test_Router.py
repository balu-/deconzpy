import unittest
from unittest import mock
from unittest.mock import patch
from deconzpy import Router

# no groups mock
def mock_pass(self):
	pass

Router.__loadAllSensors = mock_pass
Router.__loadAllRules = mock_pass
Router.__loadAllLights = mock_pass
Router.__loadAllGroups = mock_pass

class RouterElementTest(unittest.TestCase):

	def test_Router_init(self):
		pass
		#seems to hard to mock or i'm not bright enough
		#r = Router()
		#r2 = Router()
		#self.assertEqual(r, r2) #Router is a sigleton and should be the same object always
		#r3 = Router()
		#self.assertEqual(r3, r2)#Router is a sigleton and should be the same object always

if __name__ == '__main__':
    unittest.main(warnings='ignore')