#!/usr/bin/env python
#!/usr/bin/env python
from gnip_rules import GnipRules
from optparse import OptionParser
from ConfigParser import ConfigParser

config = ConfigParser()
config.read('./rules.cfg')
un = config.get('creds', 'un')
pwd = config.get('creds', 'pwd')
defaultUrl = config.get('defaults','url')

parser = OptionParser()
parser.add_option("-u", "--url", dest="url", default=None,
                        help="Input url")
(options, args) = parser.parse_args()

if options.url is not None:
    g = GnipRules(un, pwd, options.url)
    g.deleteGnipRules()
    print g.getResponse()
elif defaultUrl is not None:
    g = GnipRules(un, pwd, defaultUrl)
    g.deleteGnipRules()
    print g.getResponse()
else:
    print "No url provided."

