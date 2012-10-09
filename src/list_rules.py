#!/usr/bin/env python
from gnip_rules import GnipRules
from optparse import OptionParser
from ConfigParser import ConfigParser
from pprint import pprint

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
(options, args) = parser.parse_args()

if options.url is not None:
    r = GnipRules(un, pwd, options.url)
elif defaultUrl is not None:
    r = GnipRules(un, pwd, defaultUrl)

if options.pretty:
    pprint(r.getRules())
else:
    print r
