#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson"
__license__="Simplified BSD"

import unittest
from gnip_rule_object import * 

class TestGnipRuleObject(unittest.TestCase):
    """Unit tests for basic rules object"""
    def setUp(self):
        self.r = GnipRuleObject()

    def tearDown(self):
        self.r = GnipRuleObject()

    def test_Len(self):
        self.assertEquals(len(self.r.rules_list), 0)
        self.r.append("hello")
        self.r.append("goodbye")
        self.assertEquals(len(self.r.rules_list), 2)
        self.r.remove("hello")
        self.assertEquals(len(self.r.rules_list), 1)

    def test_Init(self):
        r = GnipRuleObject("a","b","c")
        self.assertEquals(len(r.rules_list), 3)
        r.append("hello")
        self.assertEquals(len(r.rules_list), 4)
        r = GnipRuleObject(value="goodbye", tag="goodbye_tag")
        self.assertEquals(len(r.rules_list), 1)
        self.assertTrue("value" in r.rules_list[0].keys())
        self.assertTrue("tag" in r.rules_list[0].keys())
        self.assertTrue("goodbye" in r.rules_list[0].values())
        self.assertTrue("goodbye_tag" in r.rules_list[0].values())
        r = GnipRuleObject("a", {"value":"super", "tag":"super_tag"}, value="happy", tag="happy_tag")
        self.assertEquals(len(r.rules_list), 3)
        self.assertTrue("value" in r.rules_list[0].keys())
        self.assertTrue("value" in r.rules_list[1].keys())
        self.assertTrue("value" in r.rules_list[2].keys())
        self.assertTrue(r.is_rule("a"))
        self.assertTrue(r.is_rule("happy"))
        self.assertTrue(r.is_rule("super"))

    def test_get(self):
        self.r.append("hello", "hello_tag")
        self.r.append("jello", "jello_tag")
        self.assertEquals(self.r.get(), 
                {'rules': [{'tag': 'hello_tag', 'value': 'hello'}, {'tag': 'jello_tag', 'value': 'jello'}]})


    def test_clause(self):
        r = GnipRuleObject(*[{'tag': 'hello_tag', 'value': 'hello'}, {'tag': 'jello_tag', 'value': 'jello'}])
        r.append_clause("-mello", "mello_tag")
        self.assertEquals(r.get(),
                {'rules': [{'tag': 'hello_tag:mello_tag', 'value': 'hello -mello'}, {'tag': 'jello_tag:mello_tag', 'value': 'jello -mello'}]})

    def test_valid_length(self):
        r =  GnipRuleObject("a short rule"
                , "y"*1023)
        self.assertTrue(r.valid_rule_len())
        r.append("z"*1025)
        self.assertFalse(r.valid_rule_len())

# TODO test the filter_rules

if __name__ == "__main__":
    unittest.main()
