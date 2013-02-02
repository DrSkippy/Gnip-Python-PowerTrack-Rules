#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from gnip_rules.gnip_rules import *
from gnip_rules.gnip_config import *
from optparse import OptionParser
import fileinput
import sys
import json
import codecs
# unicode
reload(sys)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)


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
    print >>sys.stderr, "No url provided. Add [defaults] url=... to config file or use -u ..."
    sys.exit()

if options.delete:
    r.deleteGnipRules()

if options.json:
    buf = ''.join([x for x in fileinput.FileInput(args,openhook=fileinput.hook_compressed)])
    r.initLocalRules()
    r.rulesList = json.loads(buf)["rules"]
else:
    r.initLocalRules()
    for row in fileinput.FileInput(args,openhook=fileinput.hook_compressed):
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
