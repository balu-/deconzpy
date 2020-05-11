import unittest
from unittest import mock
from deconzpy import Router

class RouterElementTest(unittest.TestCase):

	# no groups mock
	def mock_pass(self):
		pass

	def test_Router_init(self):
		with mock.patch.object(Router, '_Router__loadAllSensors', self.mock_pass) as mRouter:
			with mock.patch.object(mRouter, '_Router__loadAllRules', self.mock_pass) as mRouter:
				with mock.patch.object(mRouter, '_Router__loadAllLights', self.mock_pass) as mRouter:
					with mock.patch.object(mRouter, '_Router__loadAllGroups', self.mock_pass) as Router:
						r = Router()
						r2 = Router()
						self.assertEqual(r, r2) #Router is a sigleton and should be the same object always
						r3 = Router()
						self.assertEqual(r3, r2)#Router is a sigleton and should be the same object always

if __name__ == '__main__':
    unittest.main(warnings='ignore')