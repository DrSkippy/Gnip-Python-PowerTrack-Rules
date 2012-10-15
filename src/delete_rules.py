#!/usr/bin/env python
from gnip_rules import GnipRules
from optparse import OptionParser
from ConfigParser import ConfigParser
import sys

config = ConfigParser()
config.read('./rules.cfg')
un = config.get('creds', 'un')
pwd = config.get('creds', 'pwd')
defaultUrl = config.get('defaults','url')

parser = OptionParser()
parser.add_option("-u", "--url", dest="url", default=None,
                        help="Input url")
parser.add_option("-m", "--match-pattern", dest="pattern", default=None, 
            help="List only rules matching pattern (Python REs)")
parser.add_option("-t", "--match-tag", dest="matchTag", default=False, action="store_true",
            help="Match tag as well as rules (use with -m)")
parser.add_option("-d", "--delete", dest="delete", default=False, action="store_true",
                    help="Set this flag to delete, with -d, prospective changes are shown but not executed.")
(options, args) = parser.parse_args()

if options.url is not None:
    g = GnipRules(un, pwd, options.url)
elif defaultUrl is not None:
    g = GnipRules(un, pwd, defaultUrl)
else:
    print "No url provided."

if options.pattern is not None:
    g.getRulesLike(options.pattern, matchTag=options.matchTag)

if options.delete:
    print >>sys.stderr, "=== deleteing rules ==="
    g.deleteGnipRules()
    print g.getResponse()
else:
    print >>sys.stderr, "=== proposed rule deletions shown but not executed ==="
    print g

