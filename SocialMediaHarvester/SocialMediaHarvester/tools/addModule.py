'''
Created on 22.05.2014

@author: twetzel
'''

from SocialMediaHarvester import settings
import ConfigParser

name="GooglePlus"
path_to_json_conf="C:\Users\\twetzel\workspace_py\SocialMediaHarvester\SocialMediaHarvester\modules\googleplus\conf.json"

# open the config file
cfgfile = open(settings.PATH_TO_INSTALLED_HARVESTERS_INI,'ab')

# instantiate ConfigParser
config = ConfigParser.RawConfigParser()

# add new section for the module that is being installed
module_section = config.add_section(name+"Harvester")
# add key,value-pair for config file location
config.set(name+"Harvester", 'path_to_json_conf', path_to_json_conf)

config.write(cfgfile)
    
cfgfile.close()