'''
Created on 21.11.2013

@author: hauck
'''
from SocialMediaHarvester import settings
from SocialMediaHarvester.database.forms import PasswordForm, \
    UploadHarvesterForm
from SocialMediaHarvester.harvesterToolkit import installHarvester
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import ConfigParser
from symbol import parameters
from SocialMediaHarvester.settings import API_PARAMETERS


PATH_TO_HARVESTERS = settings.PATH_TO_HARVESTERS
PATH_TO_INSTALLED_HARVESTERS_TXT = settings.PATH_TO_INSTALLED_HARVESTERS_TXT

def home_view(request):
    #instantiate configParser
    config = ConfigParser.RawConfigParser()
    
    #read the config file that contains the list of all installed harvesters
    config.read(PATH_TO_INSTALLED_HARVESTERS_TXT)
    
    #get the list of installed harvesters from the config_file - every second section is a harvester
    listOfHarvesters = [str(i) for (counter, i) in list(enumerate(config.sections())) if (counter % 2 == 0)]
    
    #get the list of important parameters
    tempDict = {}
    #pre-fill the list of parameters with the API_PARAMETERS (always displayed)
    listOfParameters = API_PARAMETERS
    #iterate over the listOfHarvesters and get the parameters for each
    for h in listOfHarvesters:
        #get the supported parameters of the current harvester
        tempDict = dict(config.items(h+"Parameters"))
        
        #add the parameters to the listOfParameters if they are not duplicates and not an API_PARAMETER
        for (k, v) in tempDict.items():
            
            
            if (not v in listOfParameters) and (not k in API_PARAMETERS):
                listOfParameters.append(str(v))
        
        #empty the tempDict before restarting the for-loop
        tempDict={}
        
    #if the formular has been submitted
    if request.method == 'POST':
        paramDict = {}
        
        #iterate over request.POST (is some django class. use iteritems() to iterate it properly)
        for (paramKey, paramValue) in request.POST.iteritems(): 
            #if the first 6 characters of the key are "param_" - defined like this in the template
            if str(paramKey[:6]) == "param_":
                #add the key/value-pair to paramDict - also make sure to convert them to strings
                paramDict[str(paramKey[6:])] = str(paramValue)
        
        #get the user-selected harvesters from request.POST
        harvestersToRun = [str(i) for i in request.POST.getlist("harvesters")]
        
        #iterate over all harvesters that should run
        for h in harvestersToRun:
            #get the path to the script-file of the current harvester
            pathToScript = config.get(h, "absolute_path_to_script_file")
            
            #get all parameters the current harvester supports
            tempDict = dict(config.items(h+"Parameters"))
            
            parametersForCurrentHarvester = {}
            
            #check with which parameters harvester can work
            for (k, v) in paramDict.items():
                #if the current parameter is an api parameter and exists for the current harvester
                if k in API_PARAMETERS and k in tempDict.keys():
                    #get the name of the api_parameter for the current harvester (can be different, e.g. lat instead of latitude)
                    parametersForCurrentHarvester[tempDict[k]] = v
                    continue
                
                #if the parameter exists, add it with its actual name
                if k in tempDict.values():
                    parametersForCurrentHarvester[k] = v
            
            print "Harvester: "+h
            print "Supported Parameters: "+str(parametersForCurrentHarvester)
            print "----------------------------------------------------"
            
            #run the harvester with all its parameters
            #runPythonScript(pathToScript, **parametersForCurrentHarvester)
        
    return render_to_response('home.html', {'request':request, 'listOfHarvesters':listOfHarvesters, 'listOfParameters':listOfParameters, }, RequestContext(request))

def uploadHarvester_view(request):
    #if the form was submitted
    if request.method == 'POST':
        uploadForm = UploadHarvesterForm(request.POST, request.FILES) 
        
        #if the form is valid
        if uploadForm.is_valid():
            nameOfConfigFile = request.POST['nameOfConfigFile']
            nameOfHarvester = request.POST['nameOfHarvester']
            zippedFolder = request.FILES['zippedFolder']
            
            installHarvester(zippedFolder, nameOfConfigFile, nameOfHarvester)
            
            #save form to instance without commiting to the database
            #instance = uploadForm.save(commit=False)
            #instance can be edited here
            #save the instance
            #instance.save()    
    # if the form was not submitted, render it empty
    else:
        uploadForm = UploadHarvesterForm()
    
    return render_to_response('uploadHarvester.html', {'uploadForm': uploadForm, 'request':request, }, RequestContext(request))

def login_view(request):
    #if login-form was submitted
    if request.method == 'POST':
        #get username, password
        username = request.POST['username']
        password = request.POST['password']
        #authenticate user before logging him in - necessary!
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                #log the user in
                login(request, user)
                
                #redirect to next if it is contained in url
                if 'next' in request.GET:
                    next = request.GET['next']
                    return HttpResponseRedirect(next)
                #else, redirect to home
                else:
                    return HttpResponseRedirect("/")
            else:
                #account is disabled, return error page
                return render_to_response('registration/login.html', {'request': request, 'error_msg':'Your account is disabled. Contact us for further information.'}, RequestContext(request))
        else:
            # Return an 'invalid login' error message.
            return render_to_response('registration/login.html', {'request': request, 'error_msg':'The username or password was wrong.'}, RequestContext(request))
    
    #render blank login page        
    return render_to_response('registration/login.html', {'request': request, }, RequestContext(request))


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
