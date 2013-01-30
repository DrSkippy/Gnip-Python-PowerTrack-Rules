#!/usr/bin/env python
from gnip_rules.gnip_rules import *
from gnip_rules.gnip_config import *
from optparse import OptionParser
import sys
import csv

parser = OptionParser()
parser.add_option("-u", "--url", dest="url", default=None, help="Input url")
parser.add_option("-r", "--current-rule", dest="r1", default=None, 
            help="Rule to be replaced.")
parser.add_option("-s", "--update-rule", dest="r2", default=None, 
            help="Replacement rule.")
parser.add_option("-t", "--update-tag", dest="t2", default=None, 
            help="Replacement rule tag.")
parser.add_option("-f", "--tab-file", dest="tab", default=False, action="store_true",
            help="Stdin containing list of updates 'rule1<tab>rule2<tab>tab2'")
(options, args) = parser.parse_args()

if options.url is not None:
    g = GnipRules(un, pwd, options.url)
elif defaultUrl is not None:
    g = GnipRules(un, pwd, defaultUrl)
else:
    print >>sys.stderr, "No url provided. Add [defaults] url=... to config file or use -u ..."
    sys.exit()

if options.tab:
    for row in sys.stdin:
        [r, s, t] = row.split("\t") 
        g.updateRule(r, s, tag=t.strip())
        print g.getResponse()
elif options.r1 is not None and options.r2 is not None:
    g.updateRule(options.r1, options.r2, tag=options.t2)
    print g.getResponse()
else:
    print >>sys.stderr, "=== Use -r -s options or provide file. ==="

