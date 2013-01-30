#!/usr/bin/env python
from gnip_rules.gnip_rules import *
from gnip_rules.gnip_config import *
from optparse import OptionParser
import sys
import json
import csv

parser = OptionParser()
parser.add_option("-u", "--url", dest="url", default=None,
	help="Input url")
parser.add_option("-p", "--pretty-print", dest="pretty", default=False, action="store_true",
	help="Prettier printing of output.")
parser.add_option("-m", "--match-pattern", dest="pattern", default=None, 
    help="List only rules matching pattern (Python REs)")
parser.add_option("-t", "--match-tag", dest="matchTag", default=None,
	help="List only rules with tags matching pattern (Python REs)")
parser.add_option("-c", "--csv", dest="csv", default=False, action="store_true",
    help="Csv printing of output (with tab delimiter)")
(options, args) = parser.parse_args()

if options.url is not None:
    r = GnipRules(un, pwd, options.url)
elif defaultUrl is not None:
    r = GnipRules(un, pwd, defaultUrl)
else:
    print "No url provided. Add [defaults] url=... to config file or use -u ..."
    sys.exit()

if options.pattern is not None or options.matchTag is not None:
    r.getRulesLike(options.pattern, options.matchTag)

if options.pretty:
    print(json.dumps(r.getRules(), indent=3))
elif options.csv:
    for x in r.rulesList:
        print "%s\t%s"%(x["value"], x["tag"])
else:
    print r
