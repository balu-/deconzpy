#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from unittest.mock import Mock
from deconzpy.BaseElement import BaseElement

class VaseElementTest(unittest.TestCase):
    
    def test_dic_flattning(self):
        b1 = BaseElement(1, {"test": {"tut": {"tat": "tit"}}})
        self.assertEqual(b1.getAttribute("test_tut_tat"), "tit")

    def test_access_nonExistent(self):
    	b1 = BaseElement(1, {"test": "1"})
    	self.assertEqual(b1.getAttribute("unknown"), None)
    	self.assertEqual(b1.getAttribute("test"), "1")

    def test_subscribtion(self):
    	m = Mock()
    	m.configure_mock(name='subscribeFunction')
    	b1 = BaseElement(1, {"test": "1"})
    	b1.subscribeToAttribute('test',m)
    	m.assert_not_called() # mock should not be called on subscribe
    	b1.update({"test":"1"})
    	m.assert_not_called() # mock should not be called on same value
    	b1.update({"test":"2"})
    	m.assert_called_with(b1, 'test', '1', '2')

    def test_subscribtion_sameValue(self):
    	m = Mock()
    	m.configure_mock(name='subscribeFunction')
    	b1 = BaseElement(1, {"test": "1"})
    	b1.subscribeToAttribute('test',m, callOnlyIfValueChanged=False)
    	m.assert_not_called() # mock should not be called on subscribe
    	b1.update({"test":"1"})
    	m.assert_called_with(b1, 'test', '1', '1') # mock should  be called on same value

    def test_unsubscribe(self):
    	m1 = Mock()
    	m2 = Mock()
    	m1.configure_mock(name='subscribeFunction')
    	m2.configure_mock(name='unsubscribeFunction')
    	b1 = BaseElement(1, {"test": "1"})
    	b1.subscribeToAttribute('test',m1)
    	b1.subscribeToAttribute('test',m2)
    	m1.assert_not_called() # mock should not be called on subscribe
    	m2.assert_not_called() # mock should not be called on subscribe
    	b1.unsubscribeFromAttribute('test', m2)
    	m1.assert_not_called() # mock should not be called on unsubscribe
    	m2.assert_not_called() # mock should not be called on unsubscribe
    	b1.update({"test":"2"})
    	m1.assert_called() # mock should  be called on same value
    	m2.assert_not_called() 

    def test_unsubscribe_sameValue(self):
    	m1 = Mock()
    	m2 = Mock()
    	m1.configure_mock(name='subscribeFunction')
    	m2.configure_mock(name='unsubscribeFunction')
    	b1 = BaseElement(1, {"test": "1"})
    	b1.subscribeToAttribute('test',m1, callOnlyIfValueChanged=False)
    	b1.subscribeToAttribute('test',m2, callOnlyIfValueChanged=False)
    	m1.assert_not_called() # mock should not be called on subscribe
    	m2.assert_not_called() # mock should not be called on subscribe
    	b1.unsubscribeFromAttribute('test', m2)
    	m1.assert_not_called() # mock should not be called on unsubscribe
    	m2.assert_not_called() # mock should not be called on unsubscribe
    	b1.update({"test":"1"})
    	m1.assert_called() # mock should  be called on same value
    	m2.assert_not_called() 

if __name__ == '__main__':
    unittest.main(warnings='ignore')
