#!/bin/python

import sys  # read arguments
import os #os module
#append SocialMediaHarvester dir to path-varibale for importing smh modules
sys.path.append(os.path.abspath('/var/www/smh/html/SocialMediaHarvester/'))

# Load twython library
from twython import Twython, TwythonError, TwythonStreamer  # Load libraries for twitter API
import pymongo  # Teach python to talk to MongoDB
from time import strftime  # get system time
from optparse import OptionParser  # parse command line input parameter
from  SocialMediaHarvester import settings # smh settings
#import logging #logging framework
#log = logging.getLogger('smh') #get logger instance

# setup command line input parameter parsing
parser = OptionParser()
parser.add_option("-l", "--locations", dest="locations", default="",
                  help="Geographical Filter - Two point bounding box: longitude, latitude of south-west point followed by longitude, latitude of north-east point. Example: '-74,40,-73,41'")
parser.add_option("-t", "--track", dest="track",default="",
                  help="Keyword filter - Keywords can be connected with logical OR's and AND's surrounded by quotation marks. Example: \"#ChileEarthquake OR Chile AND Earthquake\"")
parser.add_option("-L", "--language", dest="language", default="",
                  help="Language Filter - Only tweets in the specified language are returned. Language must be specified as IETF language tag. Example: 'en' for english language")
parser.add_option("-c", "--collectionName", dest="collectionName", default="console_twitter_"+strftime("%Y%m%d%H%M%S"),
                  help="Name for the mongoDB collection in which the data is saved")

#initialize input parameter reading
(options, args) = parser.parse_args()

#set path to logfile
logpath = settings.LOG_DIR #path to twitter log folder
logfile = os.path.join(logpath,options.collectionName+'.log')

#sys.stdout = open('/var/www/smh/html/SocialMediaHarvester/SocialMediaHarvester/logs/' + options.collectionName + '.log','a')
sys.stdout = open (logfile,'a')


print('hello')

#redirect stdout to a file because apache looses all stdout
#sys.stdout = open(logfile,'a')

print('twitter harvester script launched')
sys.stdout.flush()
print(sys.argv)

#log.debug('twitter harvester script launched')
#log.debug(sys.argv)

    
# Setup authentificaion settings
APP_KEY = '28SlkUImRKk7E2GdkmxL8hoH5'  # Consumer key
APP_SECRET = 'RtrnUNFddjY5xxSr3jAGRW6kOnt9r6Mcs1GZloTaLw4tMBTsKv'  # Consumer secret

OAUTH_TOKEN = '1969113762-Ov4cNzRYvrxqdQia2gUlIQF2i1oWrm8DQWfpEmw'  # Access token
OAUTH_TOKEN_SECRET = 'v7infZXzTU3T1Q3nuNLe9gz46PP0nJNdXweb3TZSAxsKE'  # Access token secret

# Authenticate against twitter endpoint
twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()

twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

# Establish a conntection to MongoDB
client = pymongo.MongoClient('localhost', 27017)
db = client.twitter #get database
collectionName = options.collectionName
tweets = db[collectionName] #create new collection for every stream


#parse track parameter:
track = options.track

while track.find('AND') != -1 and track.find('OR') != -1:
    
    indexAND = track.find('AND')

    if indexAND != -1:
        track = track[0:indexAND - 1] + track[indexAND+ 3 :len(track)]
        
    indexOR = track.find('OR')
    
    if indexOR != -1:
        track = track[0:indexOR - 1] + "," + track[indexOR + 2:len(track)]     

# Establish streaming connection to twitter endpoint
class MyStreamer(TwythonStreamer):  # Load streaming class
    def on_success(self, data):
        if 'text' in data:
            #check if track parameter is specified
            if options.track != "":
                #if tweet contains track parameter save to database        
                if(options.track in data['text']):
                    print("found new tweet: ")
                    print(data['text'].encode('utf-8'))
                    sys.stdout.flush()
                    tweets.insert(data)
            else:
                pass
                
        # Want to disconnect after the first result?
        # self.disconnect()

    def on_error(self, status_code, data):  # Error handler
        print status_code, data
        sys.stdout.flush()

# Requires Authentication as of Twitter API v1.1
stream = MyStreamer(APP_KEY, APP_SECRET,
                    OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

#set filter
if options.locations == "":
    stream.statuses.filter(language=options.language, track=options.track)
else:
    stream.statuses.filter(language=options.language, locations=options.locations)

print "Start listening on the twitter Streaming API"
print "Saving tweets to Collection: twitter." + collectionName
sys.stdout.flush()

