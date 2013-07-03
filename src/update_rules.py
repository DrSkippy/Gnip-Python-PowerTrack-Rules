#!/usr/bin/env python
from gnip_rules.gnip_rules import *
from gnip_rules.gnip_config import *
from optparse import OptionParser
import fileinput
import sys

parser = OptionParser()
parser.add_option("-u", "--url", dest="url", default=None, help="Input url")
parser.add_option("-r", "--current-rule", dest="r1", default=None, 
            help="Rule to be replaced.")
parser.add_option("-s", "--update-rule", dest="r2", default=None, 
            help="Replacement rule (omit for tag update).")
parser.add_option("-t", "--update-tag", dest="t2", default=None, 
            help="Replacement rule tag.")
# add json processor?
(options, args) = parser.parse_args()

if options.url is not None:
    g = GnipRules(un, pwd, options.url)
elif defaultUrl is not None:
    g = GnipRules(un, pwd, defaultUrl)
else:
    print >>sys.stderr, "No url provided. Add [defaults] url=... to config file or use -u ..."
    sys.exit()

if options.r1 is not None:
    if options.r2 is not None:
        g.updateRule(options.r1, options.r2, tag=options.t2)
    else: 
        # update tag without changing rule
        g.updateRule(options.r1, options.r1, tag=options.t2)
    print g.getResponse()
else:
    for row in fileinput.FileInput(args,openhook=fileinput.hook_compressed):
        [r, s, t] = row.split("\t") 
        g.updateRule(r.strip(), s.strip(), tag=t.strip())
        print g.getResponse()

