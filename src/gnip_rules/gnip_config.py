import os
import sys
from ConfigParser import ConfigParser

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
