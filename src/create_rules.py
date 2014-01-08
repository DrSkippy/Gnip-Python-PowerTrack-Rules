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
	help="Interpret input stream as JSON rules (default is 1 text rule per line, tab separated for tags")
parser.add_option("-o", "--output-only", dest="output_only", default=False, action="store_true",
	help="Display JSON of rules that would be created with the given input file.")
parser.add_option("-d", "--delete-rules", dest="delete", default=False, action="store_true",
	help="Delete existing rules before creating new.")
parser.add_option("-a", "--append-clause", dest="post", default=None,
    help="Add this rule clause to every rule on creation (e.g. profanity negation rules or operators)")
parser.add_option("-b", "--append-tag-field", dest="post_tag", default=None,
    help="Add this field to every tag creation (e.g. project name, version or date)")
parser.add_option("-t", "--tag-field-delimiter", dest="tag_delimiter", default=":",
        help="Tag field delimiter (default is :)")
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
            r.appendLocalRule(rt[0].strip(), rt[1].strip())
        elif len(rt) == 1:
            r.appendLocalRule(rt[0].strip())
        else:
            pass

if options.post is not None or options.post_tag is not None:
    r.appendClauseToRules(options.post, options.post_tag, options.tag_delimiter)

if options.output_only:
    print r
else:
    r.createGnipRules()
    print r.getResponse()
