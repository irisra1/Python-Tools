'''
This is a script containing utility functions:
    - populateDropdown
    - mergeCharacter
    - shortenString
    - findObjects
    - findSelectedObjects
    - makeWarning
    - setTimeRange
    
'''
from PySide import QtGui, QtCore
from pyfbsdk import *
import os 

#adds items from a given directory to a dropdown 
def populateDropdown(dropdown, path):
    items = os.listdir(path)
    for p in items:
        dropdown.addItem(p)
        
#merges in a character to the current scene         
def mergeCharacter(namespace, fileName, FBApp):
    mergeOptions = FBFbxOptions(True)
    if not namespace == None:
        Names = FBStringList(str(namespace))
        mergeOptions.SetMultiLoadNamespaceList(Names)
    FBApp.FileMerge(fileName, False, mergeOptions)

#given a string and a number, removes given number of characters from the end of the string 
def shortenString(string, num):
    newString = str(string[0:(len(string)-num)])
    return newString

#given a name to search, returns a list of componenets in the scene with given name    
def findObjects(searchName):
    foundObjects = FBComponentList()
    FBFindObjectsByName(searchName, foundObjects, True, False)
    return foundObjects

#this function returns selected objects    
def findSelectedObjects():
    modelList = FBModelList()
    FBGetSelectedModels(modelList)
    return modelList
 
#pops up a warning with the specified text    
def makeWarning(warningText):    
    warningWindow = QtGui.QMessageBox()
    warningWindow.setWindowTitle('Warning')
    warningWindow.setText(warningText)
    warningWindow.exec_()

#this function creates a start and endtime FBtime object base off of given frames
#it returns the two time objects in a list    
def getTimeRange(start,end):
    startTime = FBTime(0,0,0,start,0)
    endTime = FBTime(0,0,0,end,0)
    return startTime, endTime
