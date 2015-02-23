'''
Created on 11.03.2014

@author: twetzel
'''


import datetime #time module
import subprocess, shlex #subprocess module for starting new processes
import os #os module
import json #json module
from HarvesterParameter import HarvesterParameter
from SocialMediaHarvester import settings #SMH settings
from SocialMediaHarvester.database import models #SMH database models

import logging #logging module
log = logging.getLogger('smh') #get logger instance

class Module(object):
    '''
    This class represents a Harvester module.
    It generates its data from a json config file
    '''


    def __init__(self, json_path):
        '''
        Constructor
        '''

        #open json file from specified path
        json_data = open(json_path)       
        config = json.load(json_data)
        
        #save values from json to member variables
        self.Name = config["name"]
        self.Icon = config["icon"]
        self.File = config["harvester"]
        self.Dependencies = config["dependencies"]
        self.ParameterMapping = {}
        parameter_mapping = config["parameter_mapping"]
        for i in range(len(parameter_mapping)):
            self.ParameterMapping[parameter_mapping[i]["name"]] = parameter_mapping[i]["parameter"]
        self.Parameters = []
        parameters = config["parameters"]
        for i, param in enumerate(parameters):
            self.Parameters.append(HarvesterParameter(param))
        
        json_data.close()  
        
            
    def startHarvesting(self, user, params, meta_params, collectionName):
        '''
        start the harvesting script and write the query to db
        ''' 
        
        params = self.__sortParameters(params)
        
        log.debug(self.Name + ": start harvesting...")
        
        paramString = " --collectionName=" + collectionName
        
        for param in params:
            paramString = paramString +  " --" + param + "=" + params[param]
        
        moduleDir = os.path.join(settings.PATH_TO_HARVESTERS,self.Name)
        harvesterPath = os.path.join(moduleDir,self.File)
        logDir = os.path.join(settings.LOG_DIR,collectionName+'.log')
        
        log.debug('starting script at: ' + harvesterPath)
        log.debug('with parameters: ' + paramString)
        
        #cmd = "python -u " + harvesterPath + paramString + " > " + logDir
        cmd = "python " + harvesterPath + paramString    
                
        #p = subprocess.Popen(shlex.split(cmd),shell=False, preexec_fn=os.setpgrp)
        p = subprocess.Popen(shlex.split(cmd))
        
        pid = p.pid
        
        log.debug('started harvester with pid: ' + str(pid))
              
        #generate timesamps
        stop_time = datetime.datetime.strptime(meta_params["stoptime"],'%m/%d/%Y-%H:%M')
        
        if meta_params["starttime"] == "":
            start_time =  datetime.datetime.now()
            #TODO start the q NOW
        else:
            start_time =  datetime.datetime.strptime(meta_params["starttime"],'%m/%d/%Y-%H:%M')
                
        q_query = models.query(description=meta_params["description"],owner=user,harvester=self.Name,pid=pid,isRunning=True,collectionID='',starttime=start_time,stoptime=stop_time)
        q_query.save()
        
        #save parameters to DB 
        for param in params:
            
            q_param = models.parameter(query_id=q_query.id,name=param,value=params[param])
            q_param.save()
        
        log.debug('saved query to database')         
        
        return p
            
    def getParametersToDisplay(self, listOfParameters):
        '''
        Returns only parameters which need to be displayed. 
        That means no global parameters and no parameters with subparameters.
        Requires a list to which the parameters are appended.
        '''
        
        for param in self.Parameters:
            
            #print "checking" + param.Name
            
            if(len(param.SubParameters) == 0):
                #print "has no subparameters -> append"
                if self.__mapped(param):
                    pass
                else:
                    listOfParameters.append(param)
            else:
                #print "has subparameters"
                for subParam in param.SubParameters:
                    #print subParam.Name
                    listOfParameters = self.__getSubParameters(listOfParameters, subParam)       
        
        return listOfParameters
    
    def __getSubParameters(self, listOfParameters, param):
        
        if(len(param.SubParameters) == 0):
            if self.__mapped(param):
                pass
            else:
                listOfParameters.append(param)
                
            return listOfParameters
        else:
            for subParam in param.SubParameters:
                self.__getSubParameters(listOfParameters,param)
    
    def __mapped(self,param):
        
        mapped = False

        for key in self.ParameterMapping:
            if self.ParameterMapping[key] == param.Name :
                mapped = True
        
        return mapped

    def __sortParameters(self, params):
        
        finalParams = {}
        
        for param in self.Parameters:
            if len(param.SubParameters) != 0:
                pass 
            
        finalParams = params
        
        return finalParams
    
    