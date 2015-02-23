#!/bin/python

'''
Created on 19.05.2014

@author: twetzel
'''

import datetime  # datetime module
import signal
import os
import sys 
import time
import psutil #process status module
sys.path.append(os.path.abspath('/var/www/smh/html/SocialMediaHarvester/'))
sys.path.append(os.path.abspath('../../')) #add SocialMediaHarvester module to path
os.environ["DJANGO_SETTINGS_MODULE"] = 'SocialMediaHarvester.settings' #add django settings env variable
from SocialMediaHarvester.database import models  # get database models
from SocialMediaHarvester.tools import ProcessKiller
import logging
log = logging.getLogger('smh')

log.debug('checking status of running queries...')

#get all query entries from database
queries = models.query.objects.all()

#check if there are any queries
if queries.__len__() > 0:
    
    for q in queries:
    
        #get alle queries that are marked as running
        if q.isRunning == True:
            
            pid = int(q.pid)
            log.debug('check process ' + str(pid))
            
            #check if process with pid exists
            if psutil.pid_exists(pid):
                
                #get process representation
                p = psutil.Process(int(pid))
                
                #check if proces is running
                if p.is_running:
                    if p.status() == psutil.STATUS_ZOMBIE:
                        log.debug('process is zombified')
                        q.isRunning = False;
                        q.save()
                    else:
                        #if stoptime is over and process still marked as running
                        if q.stoptime < datetime.datetime.now():
                            #kill process
                            ProcessKiller.kill_query(q)
                        pass
                else:
                    log.debug('process is not running')
                    q.isRunning = False;
                    q.save()
                
            else:
                log.debug('process does not exist')
                q.isRunning = False;
                q.save()
                
    log.debug('all queries checked.') 
           
else:
    log.debug('no queries available.')         
            
            
