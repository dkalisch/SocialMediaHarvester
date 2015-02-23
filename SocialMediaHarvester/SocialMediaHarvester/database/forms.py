'''
Created on 19.12.2012

@author: hauck
'''
from django import forms

class PasswordForm(forms.Form):
    oldPassword = forms.CharField(max_length=40, widget=forms.PasswordInput())
    newPassword1 = forms.CharField(max_length=40, widget=forms.PasswordInput())
    newPassword2 = forms.CharField(max_length=40, widget=forms.PasswordInput())
    
    oldPassword.label = "Type in your old Password"
    newPassword1.label = "Type in your new Password"
    newPassword2.label = "Retype your new Password"
    
    
class UploadHarvesterForm(forms.Form):
    nameOfHarvester = forms.CharField(max_length=40)
    zippedFolder = forms.FileField(widget=forms.ClearableFileInput, required=True)
    nameOfConfigFile = forms.CharField(max_length=40)
    
    zippedFolder.label = "Upload a zipped Harvester Folder"
    nameOfConfigFile.label = "Exact name of the Config-File (with extension! e.g.: twitter.cnf)"
    nameOfHarvester.label = "Name of the Harvester (should be the same as in the Config-File)"
    