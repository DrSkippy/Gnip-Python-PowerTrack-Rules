import os
from ConfigParser import ConfigParser

config_file_name = "./.gnip"
if 'GNIP_CONFIG_FILE' in os.environ:
    config_file_name = os.environ['GNIP_CONFIG_FILE']

config = ConfigParser()
config.read(config_file_name)
un = config.get('creds', 'un')
pwd = config.get('creds', 'pwd')
defaultUrl = config.get('defaults','url')

