'''
Created on 21.11.2013

@author: hauck
'''
import sys
def startHarvest(keyword, date):
    print "I am going to harvest for the keyword: "+keyword+", and the date: "+date+"."
    
startHarvest(sys.argv[1], sys.argv[2])