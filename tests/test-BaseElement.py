#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from deconzpy import BaseElement

class VaseElementTest(unittest.TestCase):
    
    def test_invalid_method(self):
        b1 = BaseElement(1, {"test": {"tut": {"tat": "tit"}}})
        self.assertTrue(b1.getAttribute("test_tut_tat") == "tit")

if __name__ == '__main__':
    unittest.main(warnings='ignore')
