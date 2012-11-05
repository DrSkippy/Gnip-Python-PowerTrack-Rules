#!/usr/bin/env python
from gnip_rules import GnipRules
from optparse import OptionParser
from ConfigParser import ConfigParser
import sys
import json

config = ConfigParser()
config.read('./rules.cfg')
un = config.get('creds', 'un')
pwd = config.get('creds', 'pwd')
defaultUrl = config.get('defaults','url')

parser = OptionParser()
parser.add_option("-u", "--url", dest="url", default=None,
				help="Input url")
parser.add_option("-j", "--json", dest="json", default=False, action="store_true",
				help="Interpret input stream as JSON rules")
parser.add_option("-d", "--delete-rules", dest="delete", default=False, action="store_true",
				help="Delete existing rules before creating new.")
(options, args) = parser.parse_args()

if options.url is not None:
    r = GnipRules(un, pwd, options.url)
elif defaultUrl is not None:
    r = GnipRules(un, pwd, defaultUrl)
else:
    print "No url provided."
    sys.exit()

if options.delete:
    r.deleteGnipRules()

if options.json:
    buf = sys.stdin.read()
    r.initLocalRules()
    r.rulesList = json.loads(buf)["rules"]
else:
    r.initLocalRules()
    for row in sys.stdin:
        # rule \t tag
        rt = row.split('\t')
        if len(rt) == 2:
            r.appendLocalRule(rt[0], rt[1].strip())
        elif len(rt) == 1:
            r.appendLocalRule(rt[0].strip())
        else:
            pass
r.createGnipRules()
print r.getResponse()
