'''
Created on 11.03.2014

@author: twetzel
'''

class HarvesterParameter(object):
    '''
    This class is a parameter for a harvester module.
    It can has subparameters that need to be displayed too
    '''


    def __init__(self, json):
        '''
        Constructor
        '''

        #save values from json to member variables
        self.Name = json["name"]
        self.Tooltip = json["tooltip"]
        self.Example = json["example"]
        self.IsRequired = json["isRequired"]
        self.Check = json["check"]
        subParameters = json["parameters"]
        self.SubParameters = []
        if(len(subParameters) > 0):
            for index, param in enumerate(subParameters):
                self.SubParameters.append(HarvesterParameter(param))
                
        
    def printIt(self):
        #formatted output for debugging
        print "Parameter: " + self.Name
        if(len(self.SubParameters)>0):
            for index in range(len(self.SubParameters)):
                self.SubParameters[index].printIt()