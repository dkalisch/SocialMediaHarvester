'''
Created on 11.03.2014

@author: twetzel
'''
from django.db import models
           
class query(models.Model):
    #auto generated id (primary key)
    description= models.CharField(max_length=250) #description text - displayed as title
    owner = models.CharField(max_length=50) #only the owner can see a query
    harvester = models.CharField(max_length=50) #which harvester is used
    pid = models.CharField(max_length=10) #process id
    isRunning = models.BooleanField() #is it running or not
    collectionID = models.CharField(max_length=100) #collectionID in mongoDB
    starttime = models.DateTimeField() #time the query started
    stoptime = models.DateTimeField() #time the query is going to end
    
    class Meta():
        verbose_name_plural= "queries"
    
    
class parameter(models.Model):
    query = models.ForeignKey(query) #query the parameter belongs to
    name = models.CharField(max_length=100) #name of the paremter
    value = models.CharField(max_length=500) #value of the parameer
    
    class Meta():
        verbose_name_plural= "parameters"