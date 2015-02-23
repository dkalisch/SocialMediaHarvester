'''
Created on 21.11.2013

@author: hauck
'''
from SocialMediaHarvester import settings #global settings with environment variables
import ConfigParser #parser for .ini files
import os #system library
import json #json parser

import shutil 
import zipfile

import logging
log = logging.getLogger('smh')

PATH_TO_HARVESTERS = settings.PATH_TO_HARVESTERS
# PATH_TO_INSTALLED_HARVESTERS_TXT = settings.PATH_TO_INSTALLED_HARVESTERS_TXT
PYTHON_INSTALLATION_CODE = "sudo pip install "

# new
def installModule(json_file, icon, script):
    '''
    method to install a new module:
    create new module folder and copy files to it + icon 
    create new entry in installedModules.ini
    if it fails: rollback and return False, else: return True
    '''
    
    #TODO create database
    
    success = True
    
    # open json file from specified path
    config = json.load(json_file)
    
    # set directories
    module_directory = os.path.join(PATH_TO_HARVESTERS, config['name'])
    icon_directory = os.path.join(settings.STATIC_ROOT, 'icons')
    
    
    try:
        if os.path.exists(module_directory):
            log.error('directory of the module to be installed allready exists')
            return False
        else:
            os.mkdir(module_directory) #create new directoy
            log.debug('new directory created: ' + module_directory)
    
        # write files to module folder
        path_to_json_conf = writeFileToDirectory(module_directory, json_file, str(json_file))
        writeFileToDirectory(module_directory, script, config['harvester'])
        writeFileToDirectory(icon_directory, icon, config['icon'])
    
        # generate small icon for input fields
        generateSmallIcon(icon)
    
        # add module to list of installed modules
        addModuleToInstalledModules(config['name'], path_to_json_conf)
        
        #TODO create table mongoDB
    
    except IOError as e:
        log.error("I/O error({0}): {1}".format(e.errno, e.strerror))
        success = False
    except Exception as e:
        log.error("Error at installing new harvester: " + e.strerror)
        success =  False

    if success:
        log.debug("Installed new module " + config['name'] + " terminated successfully")
        return success
    else:
        log.error("Installing new module " + config['name'] + " terminated incorrectly... rolling back")
        #if installing failed do rollback
        removeModule(config['name'])
        log.debug("rolling back terminated successfully")
        return success

def writeFileToDirectory(directory, file_data, file_name):
    '''
    write a file "file_data" with the name "file_name" to the specified directory "directory"
    '''
    
    log.debug("Wrting file " + file_name + " to " + directory)
    
    # set destination to point to the right file
    path = os.path.join(directory, file_name)
    
    # if the file already exists, dont overwrite it. return -1
    if os.path.exists(path):
        log.error("File: " + file_name + " in " + directory + " allready exists")
        raise IOError
    
    destination = open(path, 'wb')
    
    
    # write the file to the destination
    for chunk in file_data.chunks():
        destination.write(chunk)
    
    log.debug("File: " + file_name + " written successfully to " + directory)
    
    # return the absolute file path to the file    
    return path

def generateSmallIcon(icon_big):
    '''
    generate a small greyish icon from the given icon
    '''
    
    #tipp: use ImageMagick
    
    pass


def addModuleToInstalledModules(name, path_to_json_conf):
    '''
    add a new entry to installedModules.ini
    '''
    
    log.debug("adding " + name + " to installedModules.ini")
    
    # open the config file
    cfgfile = open(settings.PATH_TO_INSTALLED_HARVESTERS_INI,'ab')

    # instantiate ConfigParser
    config = ConfigParser.RawConfigParser()

    # add new section for the module that is being installed
    module_section = name+"Harvester"
    config.add_section(module_section)
    # add key,value-pair for config file location
    config.set(module_section, 'path_to_json_conf', path_to_json_conf)

    config.write(cfgfile)
    
    cfgfile.close()
    
    log.debug("added " + name + " successfully to installedModules.ini")
    
    
def removeModule(name):
    '''
    remove a complete module with folder and entry in installedModules.ini
    '''
    
    #delete folder
    
    #delete entry in ini
    
    #delete icon
    
    #delete mongoDB table
    
    pass

 


# old stuff ------------------------------------------------------------------------    
    

def installHarvester(zip, nameOfConfigFile, nameOfHarvester):
    # save the zipped folder to the harvester directory and save the absolute path
    pathToZip = writeFileToHarvesterDirectory(zip)
    
    # if the file with this name already exists
    if pathToZip == -1:
        print "File with this name already exists"
        return
    
    pathToNewFolder = extractZipFile(pathToZip, nameOfHarvester)
    
    # if the folder already exists OR the file is not a valid zip-file
    if pathToNewFolder == -1:
        print "Folder already exists or not a valid zip-file"
        return
    
    # join the path to the config file together
    pathToConfigFile = os.path.join(pathToNewFolder, nameOfConfigFile)
    
    # parse the config file
    temp = parseConfigFile(pathToConfigFile)
    # get the name of the harvester_exe 
    harvester_exe = temp[0]
    # get the parameters-dict
    paramDict = temp[1]
    # get a list of all modules that should be installed
    modules = [m for m in temp[2].values()]
    
    # join the path to the script together
    pathToScript = os.path.join(pathToNewFolder, harvester_exe)
    
    # add the harvester to the list of installed harvesters
    addHarvesterToInstalledHarvesters(nameOfHarvester, pathToConfigFile, pathToScript, paramDict)
    
    # install all relevant modules for the harvester
    installPythonModules(modules)
    
def installPythonModules(modules):
    installCommand = PYTHON_INSTALLATION_CODE
    
    for m in modules:
        installCommand += m + " "
    
    # os.system(installCommand)
    print "The following command will be executed to install the modules: " + installCommand


def addHarvesterToInstalledHarvesters(nameOfHarvester, pathToConfigFile, pathToScript, paramDict):
    # instantiate configParser
    config = ConfigParser.RawConfigParser()
    
    # open the config file
    # cfgfile = open(PATH_TO_INSTALLED_HARVESTERS_TXT,'ab')

    # create a section with the name of the harvester
    config.add_section(nameOfHarvester)
    
    # add the absolute pathes to the config and the script file to the global config file
    config.set(nameOfHarvester, "absolute_path_to_config_file", pathToConfigFile)
    config.set(nameOfHarvester, "absolute_path_to_script_file", pathToScript)
    
    # name of section that will contain the parameters for the harvester
    parameterSection = nameOfHarvester + "Parameters"
    
    # add the new section to the config-file with nameOfHarvester as section-name
    config.add_section(parameterSection)
    
    # iterate over all parameters and add them to the section
    counter = 1;
    for (k, v) in paramDict.items():
        config.set(parameterSection, k, v)
        
    # write the configfile
    # config.write(cfgfile)
    
def runPythonScript(pathToScriptFolder, scriptName, **parameters):
    bashCommand = "python " + scriptName
    
    for k, v in parameters.items():
        bashCommand += " " + str(v)
     
    print "The following command will be executed to run the harvester: " + bashCommand
    # os.system(bashCommand)

def parseConfigFile(pathToConfigFile):
    # read the config file
    config = ConfigParser.RawConfigParser()
    config.read(pathToConfigFile)

    # get the path to the harvester_exe
    harvester_exe = config.get('Harvester', 'harvester_exe')
    
    # get all parameters
    parameterDict = dict(config.items('Parameters'))
    
    # get all modules that need to be installed
    moduleDict = dict(config.items('RelevantModules'))
    
    return harvester_exe, parameterDict, moduleDict
    
# saves the uploaded files in the "Harvesters"-directory under the static root directory
def writeFileToHarvesterDirectory(f):    
    # set destination to point to the right file
    path = os.path.join(PATH_TO_HARVESTERS, str(f))
    
    # if the file already exists, dont overwrite it. return -1
    if os.path.exists(path):
        return -1
    
    destination = open(path, 'wb')
    
    
    # write the file to the destination
    for chunk in f.chunks():
        destination.write(chunk)
    
    # return the absolute file path to the file    
    return path

def extractZipFile(pathToZip, nameOfHarvester):
    pathToNewFolder = os.path.join(PATH_TO_HARVESTERS, nameOfHarvester)
    
    # if the last 4 characters aren't ".zip" or the folder already exists, don't do anything
    if not str(pathToZip[-4:]) == ".zip" or os.path.exists(pathToNewFolder):
        return -1
    
    os.makedirs(pathToNewFolder)
    
    # unzip the file at the same location
    zip = zipfile.ZipFile(pathToZip)
    unzippedFolder = zip.extractall(path=pathToNewFolder)
    zip.close()
    
    # move the zip into the created folder
    shutil.move(pathToZip, pathToNewFolder)
    
    # return the path to the new folder
    return pathToNewFolder
