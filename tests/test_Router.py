import unittest
from unittest import mock
from unittest.mock import patch
from deconzpy import Router

class RouterElementTest(unittest.TestCase):

	# no groups mock
	def mock_pass(self):
		pass

	@patch("Router.__loadAllSensors")
	@patch("Router.__loadAllRules")
	@patch("Router.__loadAllLights")
	@patch("Router.__loadAllGroups")
	def test_Router_init(self):
		r = Router()
		r2 = Router()
		self.assertEqual(r, r2) #Router is a sigleton and should be the same object always
		r3 = Router()
		self.assertEqual(r3, r2)#Router is a sigleton and should be the same object always

if __name__ == '__main__':
    unittest.main(warnings='ignore')