#!/usr/bin/env python
from gnip_rules.gnip_rules import *
from gnip_rules.gnip_config import *
from optparse import OptionParser
import sys

parser = OptionParser()
parser.add_option("-u", "--url", dest="url", default=None, help="Input url")
parser.add_option("-e", "--regex-match-rule", dest="pattern", default=None, 
    help="List only rules matching pattern (Python REs)")
parser.add_option("-x", "--regex-match-tag", dest="tagPattern", default=None, 
    help="List only rules with tag matching pattern (Python REs)")
parser.add_option("-m", "--match-rule", dest="rule", default=None, 
    help="List only rules matching rule (Exact)")
parser.add_option("-t", "--match-tag", dest="tag", default=None, 
    help="List only rules with tags matching tag (Exact)")
parser.add_option("-d", "--delete", dest="delete", default=False, action="store_true",
    help="Set this flag to delete, without -d, prospective changes are shown but not executed.")
(options, args) = parser.parse_args()

if options.url is not None:
    g = GnipRules(un, pwd, options.url)
elif defaultUrl is not None:
    g = GnipRules(un, pwd, defaultUrl)
else:
    print "No url provided. Add [defaults] url=... to config file or use -u ..."
    sys.exit()

if options.rule is not None or options.tag is not None:
    g.getRulesLike(options.rule, options.tag, req_exact=True)
elif options.pattern is not None or options.tagPattern is not None:
    g.getRulesLike(options.pattern, options.tagPattern, req_exact=False)

if options.delete:
    print >>sys.stderr, "=== Deleting rules ==="
    g.deleteGnipRules()
    print g.getResponse()
else:
    print >>sys.stderr, "=== Proposed rule deletions shown but not executed, use -d to execute ==="
    print g

