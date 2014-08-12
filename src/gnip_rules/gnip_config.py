import os
import sys
from ConfigParser import ConfigParser
"""
# REPLACED WITH UPDATED FLOW FROM SEARCH API SH 2014-08-11
config_file_name = "./.gnip"
if 'GNIP_CONFIG_FILE' in os.environ:
    config_file_name = os.environ['GNIP_CONFIG_FILE']

config = ConfigParser()
try:
    config.read(config_file_name)
    un = config.get('creds', 'un')
    pwd = config.get('creds', 'pwd')
    defaultUrl = config.get('defaults','url')
except:
    print >>sys.stderr,"########################################################################"
    print >>sys.stderr,"ERROR: Configuration file missing or fields missing!"
    print >>sys.stderr,"Check that %s exists, or you have set GNIP_CONFIG_FILE"%config_file_name
    print >>sys.stderr,"to your config file name and that your file has the proper fields."
    print >>sys.stderr,"########################################################################"
    sys.exit()
"""
DEFAULT_CONFIG_FILENAME = "./.gnip

def config_file(self):
    config = ConfigParser.ConfigParser()
    # (1) default file name precidence
    config.read(DEFAULT_CONFIG_FILENAME)
    if not config.has_section("creds"):
        # (2) environment variable file name second
        if 'GNIP_CONFIG_FILE' in os.environ:
            config_filename = os.environ['GNIP_CONFIG_FILE']
            config.read(config_filename)
    if config.has_section("creds") and config.has_section("endpoint"):
        return config
    else:
        return None

#############################################
# CONFIG FILE/COMMAND LINE OPTIONS PATTERN
# parse config file
config_from_file = self.config_file()
# set required fields to None.  Sequence of setting is:

#  (1) config file
#  (2) command line
# if still none, then fail
self.user = None
self.password = None
self.stream_url = None
if config_from_file is not None:
    try:
        # command line options take presidence if they exist
        self.user = config_from_file.get('creds', 'un')
        self.password = config_from_file.get('creds', 'pwd')
        self.stream_url = config_from_file.get('endpoint', 'url')
    except (ConfigParser.NoOptionError,
            ConfigParser.NoSectionError) as e:
        print >> sys.stderr, "Error reading configuration file ({}), ignoring configuration file.".format(e)
# parse the command line options
self.options = self.args().parse_args()
# set up the job
# over ride config file with command line args if present
if self.options.user is not None:
    un = self.options.user
if self.options.password is not None:
    pwd = self.options.password
if self.options.stream_url is not None:
    defaultUrl = self.options.stream_url
#
#############################################

