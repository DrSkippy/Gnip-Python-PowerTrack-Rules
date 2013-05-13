#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
import urllib2
import base64
import json
import sys
import re
import codecs

reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

STATUS_OK = "OK"
STATUS_ERR = "Error"
RULE_LIMIT = 5000

class RequestWithMethod(urllib2.Request):
    def __init__(self, url, method, data=None, headers={}):
        self._method = method
        urllib2.Request.__init__(self, url, data, headers)

    def get_method(self):
        if self._method:
            return self._method
        else:
            return urllib2.Request.get_method(self) 

class GnipRules(object):
    def __init__(self, UN, PWD, url):
        self.base64string = base64.encodestring('%s:%s' % (UN, PWD)).replace('\n', '')
        self.url = url
        self.initLocalRules()
        self.clean = False  # indicates sync between server 
        self.listGnipRules()

    def getResponse(self):
        return self.responseString

    def getStatus(self):
        return self.status

    def setResponse(self, x='', status=STATUS_OK):
        if status == STATUS_OK:
            self.status = True
        else:
            self.status = False
        self.responseString = ' - '.join([str(status), x.strip()])

    def initLocalRules(self):
        # creates a clean start for building records structure
        self.rulesList = []
        self.clean = False
    
    def getRules(self):
        # wraps a list of rules with dictionary structure as required
        # by Gnip's rules API
        return { "rules": self.rulesList }

    def appendClauseToRules(self, clause=None, field=None, delim = ":"):
        # append clause to every rule in the current local list
        # append field to every tag in teh current local list using delimiter
        # does not check for clean status, to allow appending to sub-set
        # of rules when combined with match
        res = []
        for x in self.rulesList:
            if clause is not None:
                val = x["value"] + " %s"%clause
            else:
                val = x["value"]
            if field is not None:
                if "tag" not in x or x["tag"] is None:
                    tag = "%s%s"%(delim, field)
                else:
                    tag = x["tag"] + "%s%s"%(delim, field)
            else:
                if "tag" not in x or x["tag"] is None:
                    tag = None
                else:
                    tag = x["tag"]
            res.append({"value":val, "tag":tag})
            self.rulesList = res

    def appendLocalRule(self, rule, tag=None):
        # Add a rule to the local list of rules
        tmp = {"value": rule, "tag": tag}
        self.rulesList.append(tmp)
        self.clean = False

    def ruleLimitRange(self):
        # Generates sublists of total rule list that comply with Gnip's
        # maximum rule update number
        for j in range(0, self.size(), RULE_LIMIT):
            if j == self.size() - 1:
                upper = self.size() % RULE_LIMIT
            else:
                upper = RULE_LIMIT 
            yield { "rules": self.rulesList[j:j + upper] }

    def listGnipRules(self):
        # When not clean, read rules for Gnip server
        if not self.clean:
            req = RequestWithMethod(self.url, 'GET')
            req.add_header('Content-type', 'application/json')
            req.add_header("Authorization", "Basic %s" % self.base64string)
            self.clean = False
            try:
                response = urllib2.urlopen(req)
                rules = json.loads(response.read(), encoding="utf-8")
                self.rulesList = rules["rules"]
                self.setResponse('%d rules returned'%self.size(), STATUS_OK)
                self.clean = True
            except urllib2.URLError:
                self.setResponse("List rules failed, check url and credentials.", STATUS_ERR)
        else:
            self.responseString = "OK"
        return self
    

    def createGnipRules(self):
        # create rules in local ruls set on the Gnip server
        if self.clean or self.rulesList == []:
            self.setResponse("No new rules to create.", STATUS_ERR)
        else:
            self.clean = False
            res = ''
            try:
                for rs in self.ruleLimitRange():
                    req = RequestWithMethod(self.url, 'POST', data=json.dumps(rs))
                    req.add_header('Content-type', 'application/json')
                    req.add_header("Authorization", "Basic %s" % self.base64string)  
                    response = urllib2.urlopen(req)
                    res += response.read()
                self.setResponse("%d rules created, %s"%(self.size(),res))
            except urllib2.URLError:
                self.setResponse("Create rules failed, check url and credentials.", STATUS_ERR)

    def deleteGnipRules(self):
        # delete rules in local rule set from Gnip server
        self.clean = False
        res = ''
        try:
            for rs in self.ruleLimitRange():
                req = RequestWithMethod(self.url, 'DELETE', data=json.dumps(rs))
                req.add_header('Content-type', 'application/json')
                req.add_header("Authorization", "Basic %s" % self.base64string)
                response = urllib2.urlopen(req)
                res += response.read()
            self.setResponse('%d rules deleted, %s'%(self.size(), res))
        except urllib2.URLError:
            self.setResponse("Delete rules failed, check url and credentials.", STATUS_ERR)

    def isRule(self, comp_rule):
        # check to see if comparative rule is in the clean local rule set
        # this is an exact string match
        if not self.clean:
            self.listGnipRules()
        for r in self.rulesList:
            if r["value"] == comp_rule:
                return True
        return False

    def updateRule(self, current_rule, updated_rule, tag=None):
        # updates are composite actions of:
        #   verify rule_old 
        #   add rule_new
        #   delete rule_old
        if not self.clean:
            self.listGnipRules()
        if self.isRule(current_rule):
            # Install new rule first so no break in stream
            self.initLocalRules()
            self.appendLocalRule(updated_rule, tag=tag)
            self.createGnipRules()
            if self.getStatus():
                # Delete old rule second
                self.initLocalRules()
                self.appendLocalRule(current_rule)
                self.deleteGnipRules()
                self.setResponse("Successfully updated %s to %s."%(current_rule, updated_rule))
            else:
                self.initLocalRules()
                self.appendLocalRule(updated_rule, tag=tag)
                self.deleteGnipRules()
                self.setResponse("Unable to install new rule, no changes made.", STATUS_ERR)
        else:
            self.setResponse("Original rule not found, please check rule and try again.", STATUS_ERR)
            

    def getRulesLike(self, rule_match_text=None, tag_match_text=None, req_exact=True):
        # list rules by approximate matches (re or sub text)
        if not self.clean:
            self.listGnipRules()
        res = []
        if rule_match_text is not None:
            ruleRE = re.compile(rule_match_text, re.IGNORECASE)
        if tag_match_text is not None:
            tagRE = re.compile(tag_match_text, re.IGNORECASE)
        for r in self.rulesList:
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
        self.rulesList = res
        self.clean = False
        return self.getRules()

    def size(self):
        # how many rules in the local list
        return len(self.rulesList)

    def __repr__(self):
        res = ''
        if not self.clean:
            res = ">>>===SHOWING LOCAL RULES -- May NOT RELECT SERVER STATUS===<<<\n"
        return res + json.dumps(self.getRules(), encoding="utf-8")

if __name__ == '__main__':
    Url = 'rules management url'
    Un = 'username'
    Pwd = 'password'
    
    print "Testing against: %s"%Url
    
    r = GnipRules(Un, Pwd, Url)
    print r
    print r.getResponse()

    tmpr = r.getRules()
    r.deleteGnipRules()
    print r
    print r.getResponse()

    r.initLocalRules()
    r.createGnipRules()
    print r.getResponse()

    r.rulesList = tmpr["rules"]
    r.createGnipRules()
    print r.getResponse()
    print r.listGnipRules()

    r.appendLocalRule("rule1", "myTag1")
    r.appendLocalRule("rule2")
    r.appendLocalRule("and yet another rule", "with a tag string this time")
    print r
    r.appendLocalRule("rule3","myTag3")
    r.createGnipRules()
    print r.listGnipRules()
    
    r.initLocalRules()
    r.appendLocalRule("rule3","myTag3")
    r.deleteGnipRules()
    print r.listGnipRules()

    print r.isRule("rule")
    print r.isRule("hello")
    print r.getRuleLike("2")
    print r.getRuleLike("tag", match_tag=True)
