#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
import sys
import re
import codecs
import time

reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

RULE_LEN_LIMIT = 1024

class GnipRuleObject(object):
    def __init__(self, *args, **kwargs):
        """Contstruct an object with any of::
               Empty, no arguements
               args as rule values
               args as {"value":value, "tag":tag} dictionaries
               value=value, tag=tag keyword args"""
        self.rules_list = []
        if kwargs != {}:
            self.rules_list.append(kwargs)
        for v in args:
            if isinstance(v, dict):
                self.rules_list.append(v)
            else:
                self.rules_list.append({"value":v})

    def append(self, rule, tag=None):
        """Add a rule to the list"""
        tmp = {"value": rule }
        if tag is not None:
            tmp["tag"] = tag
        self.rules_list.append(tmp)

    def remove(self, rule, tag=None):
        """Remove a single rule form the list by value or tag match"""
        res = []
        for r in self.rules_list:
            if tag is None and r["value"] != rule:
                res.append(r)
            elif tag is not None:
                if tag != r["tag"] or rule != r["value"]:
                    res.append(r)
        self.rules_list = res

    def get(self):
        """ wraps a list of rules with dictionary structure as required
        by Gnip's rules API"""
        return { "rules": self.rules_list }

    def append_clause(self, clause=None, field=None, delim = ":"):
        """append clause to every rule in the current local list
        append field to every tag in teh current local list using delimiter
        does not check for clean status, to allow appending to sub-set
        of rules when combined with match"""
        res = []
        for x in self.rules_list:
            if clause is not None:
                val = x["value"] + " %s"%clause
            else:
                val = x["value"]
            if field is not None:
                if "tag" not in x or x["tag"] is None:
                    tag = "%s"%(field)
                else:
                    tag = x["tag"] + "%s%s"%(delim, field)
            else:
                if "tag" not in x or x["tag"] is None:
                    tag = None
                else:
                    tag = x["tag"]
            res.append({"value":val, "tag":tag})
            self.rules_list = res

    def valid_rule_len(self):
        valid = True
        cnt = 0
        for r in self.rules_list:
            cnt += 1
            if len(r["value"]) > RULE_LEN_LIMIT:
                valid = False
                print >>sys.stderr,"Error with rule (%4d): %s"%(cnt,r["value"])
        return valid

    def is_rule(self, comp_rule):
        """check to see if comparative rule is in the clean local rule set
        this is an exact string match"""
        for r in self.rules_list:
            if r["value"] == comp_rule:
                return True
        return False

    def filter_rules(self, rule_match_text=None, tag_match_text=None, req_exact=True):
        """list rules by approximate matches (re or sub text)"""
        res = []
        if rule_match_text is not None:
            ruleRE = re.compile(rule_match_text, re.IGNORECASE)
        if tag_match_text is not None:
            tagRE = re.compile(tag_match_text, re.IGNORECASE)
        for r in self.rules_list:
            matched = False
            exact = False
            if tag_match_text is not None and "tag" in r and r["tag"] is not None:
                tmp =  tagRE.search(r["tag"])
                if tmp:
                    matched = True
                    if tmp.group(0) == r["tag"]:
                        exact = True
            if rule_match_text is not None and "value" in r:
                tmp =  ruleRE.search(r["value"])
                if tmp:
                    matched = True
                    if tmp.group(0) == r["value"]:
                        exact = True
            if matched:
                if req_exact:
                    if exact:
                        res.append(r)
                else:
                    res.append(r)
        self.rules_list = res

    def __len__(self):
        # how many rules in the local list
        return len(self.rules_list)

    def __repr__(self):
        return json.dumps(self.get(), encoding="utf-8")
