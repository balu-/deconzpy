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
			di["key1"] = dict()
			di["key1"]["key2"] = 3
			l = Light.Light(0, di, 'base/URL') # just create a trash obj
			self.assertTrue(l.hasState(0)) #make sure state 0 is initaly there






if __name__ == '__main__':
    unittest.main(warnings='ignore')