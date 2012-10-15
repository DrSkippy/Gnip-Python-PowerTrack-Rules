#!/usr/bin/env python
from gnip_rules import GnipRules
from optparse import OptionParser
from ConfigParser import ConfigParser
import json

config = ConfigParser()
config.read('./rules.cfg')
un = config.get('creds', 'un')
pwd = config.get('creds', 'pwd')
defaultUrl = config.get('defaults','url')

parser = OptionParser()
parser.add_option("-u", "--url", dest="url", default=None,
	help="Input url")
parser.add_option("-p", "--pretty-print", dest="pretty", default=False, action="store_true",
	help="Prettier printing of output.")
parser.add_option("-m", "--match-pattern", dest="pattern", default=None, 
    help="List only rules matching pattern (Python REs)")
parser.add_option("-t", "--match-tag", dest="matchTag", default=False, action="store_true",
	help="Match tag as well as rules (use with -m)")
(options, args) = parser.parse_args()

if options.url is not None:
    r = GnipRules(un, pwd, options.url)
elif defaultUrl is not None:
    r = GnipRules(un, pwd, defaultUrl)

if options.pattern is not None:
    r.getRulesLike(options.pattern, matchTag=options.matchTag)

if options.pretty:
    print(json.dumps(r.getRules(), indent=3))
else:
    print r
