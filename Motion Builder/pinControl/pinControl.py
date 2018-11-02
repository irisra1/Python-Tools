'''
This script contains a class that pins controls and generates a simple UI.
The class contains these functions:
    -makeUI()
    -connectSignals()
    -findControl()
    -getAnimNodes()
    -getKeyValue(transform, axis, time, animNode)
    -timeCheck()
    -frameNumberCheck()
    -zeroKey()
    -setKeyValue()
    -buttonPressed()
    -bakeButtonPressed()
'''
#----------------
#imports
#----------------
from pyfbsdk import *
import os
from PySide import QtGui, QtCore

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

#class for making the UI and pinning controls 
class pinControlUI(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(pinControlUI, self).__init__(parent)
        self.makeUI()
        self.show()
        self.connectSignals()
        
    #this function makes a simple UI     
    def makeUI(self):
        #makes the main window 
        self.window = QtGui.QWidget()
        self.setWindowTitle('Pin Control')
        self.resize(350, 175)
        self.setMaximumSize(350, 175)
        self.setMinimumSize(350, 175)
        self.verticalWindowLayout = QtGui.QVBoxLayout(self.window)
        
        #makes a frame
        self.frame = QtGui.QFrame(self.window)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.verticalFrameLayout = QtGui.QVBoxLayout(self.frame)
        
        #makes label and text box for holding current selected control 
        self.label = QtGui.QLabel()
        self.label.setText('Selected Control:')
        self.horizontalCtrlLayout = QtGui.QHBoxLayout()
        self.horizontalCtrlLayout.addWidget(self.label)
        self.verticalFrameLayout.addLayout(self.horizontalCtrlLayout)
        
        #make a line edit to contain the name of the selected control 
        self.textBox = QtGui.QLineEdit()
        self.textBox.setReadOnly(True)
        self.horizontalCtrlLayout.addWidget(self.textBox)
        
        #makes a button to select a control 
        self.button = QtGui.QPushButton()
        self.button.setText('select')
        self.horizontalCtrlLayout.addWidget(self.button) 
        
        #makes a line to seperate selecting the control from pinning it 
        self.line = QtGui.QFrame()
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.verticalFrameLayout.addWidget(self.line)
        
        #makes a button to execute pinning the control 
        self.pinButton = QtGui.QPushButton()
        self.pinButton.setText('Pin Control')
        self.pinButton.setMinimumSize(310, 35)
        self.pinButton.setMaximumSize(310, 35)
        self.verticalFrameLayout.addWidget(self.pinButton)
        
        #adds a dividing line
        self.lowerLine = QtGui.QFrame()
        self.lowerLine.setFrameShape(QtGui.QFrame.HLine)
        self.lowerLine.setFrameShadow(QtGui.QFrame.Sunken)
        self.verticalFrameLayout.addWidget(self.lowerLine)
        
        #makes a button for baking down animation 
        self.bakeButton = QtGui.QPushButton()
        self.bakeButton.setText('Bake Animation')
        self.bakeButton.setMinimumSize(310, 35)
        self.bakeButton.setMaximumSize(310, 35)
        self.verticalFrameLayout.addWidget(self.bakeButton)

        self.verticalWindowLayout.addWidget(self.frame)
        self.setCentralWidget(self.window)
    
    #connects signal for the UI
    def connectSignals(self):
         QtCore.QObject.connect(self.button, QtCore.SIGNAL('clicked()'), self.buttonPressed)
         QtCore.QObject.connect(self.pinButton, QtCore.SIGNAL('clicked()'),self.setKeyValue)
         QtCore.QObject.connect(self.bakeButton, QtCore.SIGNAL('clicked()'), self.bakeButtonPressed)
    
    #checks for selected controls 
    def findControl(self):
        self.selected = findSelectedObjects()
        if len(self.selected) > 1:
            makeWarning('More than one object selected. Please select one control to continue.')
        elif len(self.selected)< 1:
            makeWarning('No control selected. Please select one control to continue.')
        
        return self.selected
    #gets animation node for translation and rotation         
    def getAnimNodes(self):
        self.control = self.findControl()[0]
        #get anim node for translation 
        transNode = self.control.Translation.GetAnimationNode()
        #get anim node for rotation 
        rotNode = self.control.Rotation.GetAnimationNode()
        return transNode, rotNode
    
    #gets value of given key at given time from a given animation node    
    def getKeyValue(self,transform, axis, time, animNode):
        valueAxis = animNode[transform].Nodes[axis].FCurve
        value = valueAxis.Evaluate(time)
        return value
        
    #checks if start frame is valid     
    def timeCheck(self):
        timeValid = True
        self.system.CurrentTake.SetCurrentLayer(0)
        self.baseAnimNodes = self.getAnimNodes()
        #finds the first key on the base animation curve
        firstFrame = self.baseAnimNodes[0].Nodes[0].FCurve.Keys[0].Time
        #finds the last key on the base animation curve
        lastFrame = self.baseAnimNodes[0].Nodes[0].FCurve.Keys[len(self.baseAnimNodes[0].Nodes[0].FCurve.Keys)-1].Time
        #checks that the keys to be edited are in range of the base animation
        if self.startTime < firstFrame or  self.endTime > lastFrame:
            makeWarning('Frame range is not valid.')
            timeValid = False
       
        return timeValid
        
    #checks to make sure that the right number of keys are set     
    def frameNumberCheck(self):
        frameNum = True 
        #checks if there are fewer than 2 keys on pin layer
        if len(self.animLayerNodes[0].Nodes[0].FCurve.Keys) < 2:
            frameNum = False
            makeWarning('Not enough keys')
        #checks is there are more than keys on pin layer
        elif len(self.animLayerNodes[0].Nodes[0].FCurve.Keys) > 2:
            frameNum = False
            makeWarning('too many keys')
            
        return frameNum
        
    #adds a base key at the end of the hold to blend into the rest of the animation     
    def zeroKey(self):
        #gets the key to adjust 
        setKey = self.endTime + FBTime(0,0,0,5,0) 

        #sets a key with the same value as the first animation layer key
        for i in range(2):
            for j in range(3):
                setValue = self.getKeyValue(i, j, self.startTime, self.animLayerNodes)
                self.animLayerNodes[i].Nodes[j].FCurve.KeyAdd(setKey,setValue) 
                
    #this function sets keys pinning the control in place     
    def setKeyValue(self):
        #gets anim nodes for translation and rotation 
        self.animLayerNodes = self.getAnimNodes()
        #gets FBTime objects for given frames 
        self.startTime = self.animLayerNodes[0].Nodes[0].FCurve.Keys[0].Time
        self.endTime = self.animLayerNodes[0].Nodes[0].FCurve.Keys[len(self.animLayerNodes[0].Nodes[0].FCurve.Keys)-1].Time
        
        #gets frame numbers for the keys
        self.startFrame = self.startTime.GetFrame()
        self.endFrame = self.endTime.GetFrame() 
        
        #checks that given frames are in a valid time range
        frameNum = self.frameNumberCheck()
        valid = self.timeCheck() 

         
        if valid and frameNum:
            #FBTime to be incremented in the for loop 
            incTime = self.startTime
            #sets new keys in a loop
            for key in range(self.startFrame, self.endFrame):
                #adds one frame to current time 
                incTime += FBTime(0,0,0,1,0)
                #sets new keys for all three fcurves for rotation and translation  
                for i in range(2):
                    for j in range(3):
                        self.system.CurrentTake.SetCurrentLayer(0)
                        firstValue = self.getKeyValue(i, j, self.startTime, self.baseAnimNodes)
                        currentValue = self.getKeyValue(i, j, incTime, self.baseAnimNodes)
                        setValue = firstValue - currentValue 
                        self.system.CurrentTake.SetCurrentLayer(self.numLayers-1)
                        self.animLayerNodes[i].Nodes[j].FCurve.KeyAdd(incTime, setValue)
            #blend end of hold
            self.zeroKey()
 
    #when button is pressed makes a new anim layer and renames the layer 
    #and sets it to be the active layer         
    def buttonPressed(self):
        #makes a new animation layer 
        self.system = FBSystem()
        self.system.CurrentTake.CreateNewLayer()
        #gets the number of animation layers
        self.numLayers = self.system.CurrentTake.GetLayerCount()
        #gets the name of the selected control 
        ctrlName = str(self.findControl()[0].Name)
        #renames the layer to match the control name 
        self.system.CurrentTake.GetLayer(self.numLayers-1).Name = ctrlName
        #sets the new layer as the active layer
        self.system.CurrentTake.SetCurrentLayer(self.numLayers-1) 
        self.textBox.setText(ctrlName)
    #bakes layers together into the base animation layer     
    def bakeButtonPressed(self):
        #set up merge options 
        mergeOptions = FBAnimationLayerMergeOptions(2)
        deleteLayers = True         
        layerMode = FBMergeLayerMode(True)
        
        #selects the base animation layer and the pin layer
        baseLayer = self.system.CurrentTake.GetLayer(0)
        FBAnimationLayer.SelectLayer(baseLayer, True, True)
        pinLayer = self.system.CurrentTake.GetLayer(self.numLayers -1)
        FBAnimationLayer.SelectLayer(pinLayer, True, False)
        #merge the two layers together 
        self.system.CurrentTake.MergeLayers(mergeOptions, deleteLayers, layerMode) 
        
        
test = pinControlUI()
