'''
Created on 21.11.2013

@author: hauck
'''

from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

import logging # Logging module for writing log entries
import ConfigParser # Parsing config files like .ini
import json # parsing and creating .json files
import pymongo  # Teach python to talk to MongoDB
from time import strftime #get current time

from SocialMediaHarvester.tools import ProcessKiller
from SocialMediaHarvester.module import HarvesterToolkit
from SocialMediaHarvester.database import models
from SocialMediaHarvester import settings
from SocialMediaHarvester.database.forms import PasswordForm, \
    UploadHarvesterForm
from SocialMediaHarvester.module.Module import Module
from SocialMediaHarvester.module.HarvesterParameter import HarvesterParameter

#get specified logger with the name 'smh'
log = logging.getLogger("smh")

def home_view(request):
    
    log.debug('home_view requested...')
    
    #get all installed modules
    modules = get_modules()

    #instantiate empty dict for parameters
    listOfParameters = {}    
  
    #iterate over modules and write them with parameters to dict
    for module in modules:
        #key = modul name, value = parameter array
        listOfParameters[module.Name] = (module.getParametersToDisplay([]))
    
            #global parameters
        #set path to global parameters
        json_path = settings.PATH_TO_GLOBAL_PARAMTERS_JSON
        #open json file at 'json_path'
        json_data = open(json_path)
        #read json data      
        parameters = json.load(json_data)
        
        #get parameters section from json
        globalParameters_json =  parameters["parameters"]
        #instantiate empty array for global parameters
        globalParameters = []
    
        #iterate over parameters and append to 'globalParameters' array
        for param in globalParameters_json:
            #create new HarvesterParameter instance from every parameter in json file
            globalParameters.append(HarvesterParameter(param))
    
        #write global parameters to dict with key 'global'
        listOfParameters["global"] = globalParameters 

        #meta parameters
        #set path to meta parameters
        json_path = settings.PATH_TO_META_PARAMTERS_JSON
        #open json file at 'json_path'
        json_data = open(json_path)
        #read json data      
        parameters = json.load(json_data)
        
        #get parameters section from json
        metaParameters_json =  parameters["parameters"]
        #instantiate empty array for meta parameters
        metaParameters = []
        
        #iterate over parameters and append to 'metaParameters' array
        for param in metaParameters_json:
            #create new HarvesterParameter instance from every parameter in json file
            metaParameters.append(HarvesterParameter(param))
        
        #write meta parameters to dict with key 'meta'
        listOfParameters["meta"] = metaParameters

    #if the formular has been submitted
    if request.method == 'POST':

        log.debug('request to start new query has been submitted')
        
        #get q data        
        queryDict = request.POST
        log.debug(queryDict)
        #queryDict.iteritems()

        #get user-selected harvesters
        harvestersToRun = queryDict.getlist("selectedHarvesters")
        
        #container for the meta parameters
        meta_parameters = {}
             
        #name of the collections in mongoDB
        collectionName=request.user.username+"_"+strftime("%Y%m%d%H%M%S")
        
        for paramKey, paramValue in queryDict.iteritems():
            #append meta parameters
            if "param_meta" in paramKey:
                splittedKey = str(paramKey).split("_")
                #print splittedKey[2]              
                print queryDict.getlist(str(paramKey))
                #print paramKey      
                #print queryDict[str(paramKey)]
                meta_parameters[splittedKey[2]] = queryDict[paramKey]
             
        #iterate over harvesters to select parameters from query data   
        for harvester in harvestersToRun:
            log.debug('selected harvester: ' + harvester)
            
            #container for the parameters
            parameters = {}

            #search for all parameters with the harvester name in key
            for paramKey, paramValue in queryDict.iteritems():
                
                #append harvester parameters
                if harvester in paramKey and "param_" in paramKey:
                    
                    log.debug('parameter: ' + paramKey + ": " + paramValue)                    
                    #split string at "_"
                    #[0] = "params_"; [1] = harvester name; [2] = parameter name
                    splittedKey = str(paramKey).split("_")
                    #print splittedKey[2]              
                    #print paramValue                      
                    parameters[splittedKey[2]] = paramValue
            
            #get the mapped global parameters:
            #iterate over module objects
            for module in modules:
                #if the right module class is found
                if module.Name == harvester:
                    #iterate over parameter mapping dict
                    for key, value in module.ParameterMapping.items():
                        #select mapped global parameters and write to parameters 
                        #value = parameter name for harvester
                        #key = name of global parameter
                        if key == "keyword":                                            
                            parameters[value] = '"' + queryDict["param_global_" + key] + '"'
                        else:
                            parameters[value] = queryDict["param_global_" + key]
                    
                    log.debug('query parameters:')
                    log.debug(parameters)
                    #start harvesting        
                    module.startHarvesting(request.user,parameters,meta_parameters,collectionName)
                    
        return render_to_response('success.html', {'message':"Query was created successfully"}, RequestContext(request))
       
    return render_to_response('home.html', {'request':request,'listOfParameters':listOfParameters,'modules':modules, }, RequestContext(request))

@login_required
def uploadHarvester_view(request):
    #if the form was submitted
    if request.method == 'POST':
        uploadForm = UploadHarvesterForm(request.POST, request.FILES) 
        
        #if the form is valid
        if uploadForm.is_valid():
            
            json_file = request.FILES['json_file']
            icon = request.FILES['icon']
            script = request.FILES['script']

            success = HarvesterToolkit.installModule(json_file, icon, script)
            
            if(success):
                return render_to_response('success.html', {'message':'Added new harvester successfully'}, RequestContext(request))
            else:
                return render_to_response('error.html', {'message':'Adding new harvester failed'}, RequestContext(request))
            #save form to instance without commiting to the database
            #instance = uploadForm.save(commit=False)
            #instance can be edited here
            #save the instance
            #instance.save()    
    # if the form was not submitted, render it empty
    else:
        uploadForm = UploadHarvesterForm()
    
    return render_to_response('uploadHarvester.html', {'uploadForm': uploadForm, 'request':request}, RequestContext(request))

@login_required
def query_view(request):
    
    #if a request has been submitted
    if request.method == 'POST':
        log.debug("cancelling query request submitted")
        queryDict = request.POST
        log.debug(queryDict)
        #kill process with process id pid
        ProcessKiller.kill_pid(queryDict['query_pid'])
    
    #create a database q that gets all queries from the database which have the current user as their owner
    #the variable 'queries' hold the result of the database q
    queries = models.query.objects.filter(owner=request.user)
    
    #instantiate empty array for the params of the queries
    params = []
    
    #iterate over all found queries
    for q in queries:
        #unleash a database q that gets all the parameters thet belong to a q found with the previous database q
        parameters = models.parameter.objects.filter(query_id=q.id)
        for param in parameters:
            #iterate over the parameters that have been found and append them to 'params'-array
            params.append(param)    
    
    #for future use:    
    # Establish a conntection to MongoDB
    mongoDB = settings.DATABASES['mongoDB']
    
    client = pymongo.MongoClient(mongoDB['HOST'], mongoDB['PORT'])
    db = client.twitter #get database
    collections = db.collection_names() #get the collections by name
    
    #TODO: maybe load collections that hold the data of the found queries and display them for the user      
    
    return render_to_response('query.html',{'collections': collections, 'queries': queries, 'params': params},RequestContext(request))

@login_required
def configuration_view(request):
    
    #get all installed modules
    modules = get_modules()
    
    return render_to_response('configuration.html',{'modules': modules},RequestContext(request))

def login_view(request):
    #if login-form was submitted
    if request.method == 'POST':
        #get username, password
        username = request.POST['username']
        password = request.POST['password']
        #authenticate user before logging him in - necessary!
        user = authenticate(username=username, password=password)
        
        if user is not None:
            print"user is authenticated"
            if user.is_active:
                #log the user in
                login(request, user)
                
                #redirect to next if it is contained in url
                if 'next' in request.GET:
                    next = request.GET['next']
                    return HttpResponseRedirect(next)
                #else, redirect to home
                else:
                    print "alles ok"
                    return HttpResponseRedirect("/")
            else:
                #account is disabled, return error page
                return render_to_response('registration/login.html', {'request': request, 'error_msg':'Your account is disabled. Contact us for further information.'}, RequestContext(request))
        else:
            # Return an 'invalid login' error message.
            return render_to_response('registration/login.html', {'request': request, 'error_msg':'The username or password was wrong.'}, RequestContext(request))
    
    #render blank login page        
    return render_to_response('registration/login.html', {'request': request, }, RequestContext(request))

@login_required
def logout_view(request):
    auth.logout(request)
    # Redirect to a success page.
    return render_to_response('registration/logout.html', {'request': request, }, RequestContext(request))


@login_required
def password_view(request):
    error = ""
    success = ""
    pForm = PasswordForm()

    if request.method == 'POST':
        if request.POST['submit'] == 'Change':
            pForm = PasswordForm(request.POST)
            if pForm.is_valid():
                oldPass = request.POST['oldPassword']
                newPass1 = request.POST['newPassword1']
                newPass2 = request.POST['newPassword2']
                if newPass1 == newPass2 and request.user.check_password(oldPass):
                    user = request.user
                    user.set_password(newPass1)
                    user.save()
                    success = "Your password was successfully changed!"
                else:
                    if not request.user.check_password(oldPass):
                        error = "The old password was incorrect."
                    else:
                        error = "The new passwords didn't match."
                    pForm = PasswordForm()

    return render_to_response('registration/change_password.html', {'pForm':pForm, 'error':error, 'success':success, }, RequestContext(request))

#helper method that returns all installed modules
def get_modules():
    
    #instantiate ConfigParser
    config = ConfigParser.RawConfigParser()
    #set path to config file
    print str(settings.PATH_TO_INSTALLED_HARVESTERS_INI)
    config_path = str(settings.PATH_TO_INSTALLED_HARVESTERS_INI)
    #read config file at patch 'config_path'
    config.read(config_path)

    #instantiate empty array for installed modules
    modules = []
    
    #fill array with modules from config file
    for harvester in config.sections():
        #create new Module instance with path to the json config and append to 'modules' array
        modules.append(Module(config.get(harvester, "path_to_json_conf")))
        
    return modules;