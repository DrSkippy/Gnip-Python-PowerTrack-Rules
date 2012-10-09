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

	def getSuccess(self):
		return self.status

	def setResponse(self, x='', status=STATUS_OK):
		if status == STATUS_OK:
			self.status = True
		else:
			self.status = False
		self.responseString = ' - '.join([str(status), x.strip()])

	def initLocalRules(self):
		self.rulesList = []
		self.clean = False
	
	def getRules(self):
		return { "rules": self.rulesList }

	def appendLocalRule(self, rule, tag=None):
		tmp = {"value": rule, "tag": tag}
		self.rulesList.append(tmp)
		self.clean = False

	def ruleRange(self):
		for j in range(0, self.size(), RULE_LIMIT):
			if j == self.size() - 1:
				upper = self.size() % RULE_LIMIT
			else:
				upper = RULE_LIMIT 
			yield { "rules": self.rulesList[j:j + upper] }

	def listGnipRules(self):
		if not self.clean:
			req = RequestWithMethod(self.url, 'GET')
			req.add_header('Content-type', 'application/json')
			req.add_header("Authorization", "Basic %s" % self.base64string)
			try:
				response = urllib2.urlopen(req)
				rules = json.loads(response.read(), encoding="utf-8")
				self.rulesList = rules["rules"]
				self.setResponse('%d rules returned'%self.size(), STATUS_OK)
				self.clean = True
			except urllib2.URLError:
				self.clean = False
				self.setResponse("List rules failed, check url and credentials.", STATUS_ERR)
		else:
			self.responseString = "OK"
		return self
	

	def createGnipRules(self):
		if self.clean:
			self.setResponse("No new rules to create.", STATUS_ERR)
		else:
			self.clean = False
			res = ''
			try:
				for rs in self.ruleRange():
					req = RequestWithMethod(self.url, 'POST', data=json.dumps(rs))
					req.add_header('Content-type', 'application/json')
					req.add_header("Authorization", "Basic %s" % self.base64string)  
					response = urllib2.urlopen(req)
					res += response.read()
				self.setResponse("%d rules created, %s"%(self.size(),res))
			except urllib2.URLError:
				self.setResponse("Create rules failed, check url and credentials.", STATUS_ERR)

	def deleteGnipRules(self):
		self.clean = False
		res = ''
		try:
			for rs in self.ruleRange():
				req = RequestWithMethod(self.url, 'DELETE', data=json.dumps(rs))
				req.add_header('Content-type', 'application/json')
				req.add_header("Authorization", "Basic %s" % self.base64string)
				response = urllib2.urlopen(req)
				res += response.read()
			self.setResponse('%d rules deleted, %s'%(self.size(), res))
			self.initLocalRules()
		except urllib2.URLError:
			self.setResponse("Delete rules failed, check url and credentials.", STATUS_ERR)

	def isRule(self, key, match_tag=False):
		if self.getRuleMatchCount(key, match_tag) > 0:
			return True
		else:
			return False

	def getRuleMatchCount(self, key, match_tag=False):
		if not self.clean:
			self.listGnipRules()
		res = 0
		ruleMatch = re.compile(key, re.IGNORECASE)
		for r in self.rulesList:
			if ruleMatch.search(r["value"]):
				res += 1
			elif match_tag and r["tag"] is not None and ruleMatch.search(r["tag"]):
				res += 1
		return res

	def size(self):
		return len(self.rulesList)

	def __repr__(self):
		res = ''
		if not self.clean:
			res = "===LOCAL===\n"
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
	print r.getRuleMatchCount("2")
	print r.getRuleMatchCount("tag", match_tag=True)
	print r.isRule("hello")
