#!/usr/bin/env python
from gnip_rules.gnip_rules import *
from gnip_rules.gnip_config import *
from optparse import OptionParser
import sys
import json

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
    print "No url provided. Add [defaults] url=... to config file or use -u ..."
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
