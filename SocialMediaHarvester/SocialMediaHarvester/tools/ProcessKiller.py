'''
Created on 21.05.2014

@author: twetzel
'''
import os
import signal
import psutil
import sys
import time
sys.path.append(os.path.abspath('../../')) #add SocialMediaHarvester module to path
os.environ["DJANGO_SETTINGS_MODULE"] = 'SocialMediaHarvester.settings' #add django settings env variable
from SocialMediaHarvester.database import models  # get database models
import logging
log = logging.getLogger('smh')

def kill_pid(pid):
    log.debug("killing process: " + str(pid))
    
    queries = models.query.objects.all().filter(pid=pid)
    
    for q in queries:
        if psutil.pid_exists(int(q.pid)):
            log.debug('process does not exist') 
            kill_query(q)
        
            
def kill_query(q):
    
    pid = int(q.pid)
    log.debug("killing query: " + q.description + " (" + str(pid) + ")")
    
    try:    
               
        # kill process with hole group (necessary?)
        os.kill(int(pid), 9)
        #os.killpg(pid, signal.SIGTERM)
        time.sleep(3)
                        
        # get process psutil representation
        p = psutil.Process(pid)
        pp = p.parent()
                           
        if p.is_running():
            log.debug('still running')
                            
            if p.status() == psutil.STATUS_ZOMBIE:
                log.debug('zombified with parent ' + str(pp.pid))
                q.isRunning = False;
                q.save()            
            else:
                log.debug('terminating failed - trying again')
                # try killing again with other command
                # may be necessary if apache died
                os.kill(int(pid), 9)
                time.sleep(3)
                                
                # check if process is running 
                if os.path.exists(os.path.join('/proc/', str(pid))):
                    log.debug('terminating failed')
                else:
                    q.isRunning = False;
                    q.save()            
                    log.debug('terminated.')
        else:
            log.debug('terminated.')
            q.isRunning = False;
            q.save()  
                          
    except OSError as e:
        log.error('Exception: %s' % e)
        q.isRunning = False;
        q.save()  
    except psutil.NoSuchProcess as e:
        log.error('Exception: %s' % e)
        q.isRunning = False;
        q.save() 
                