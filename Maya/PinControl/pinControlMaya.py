'''
This script contains a class that pins a control and makes a simple UI to tell the user what control 
was pinned. 
It contains these functions:
    -getMayaWindow()
    -makeUI()
    -connectSignals
    -getControl()
    -getKeyValue(time, animCurve)
    -isValid()
    -setKeys()
    -zeroKey()
    -buttonPressed()
    -bakeButtonPressed()
    -frameNumberCheck()
'''
#------------
#imports
#------------
import maya.OpenMayaUI as omui
import pymel.core as pm 
#this makes the tool compatible in both 2014 and 2018
try:
    from PySide2 import QtGui, QtCore, QtWidgets
    from shiboken2 import wrapInstance
   
except: 
    from shiboken import wrapInstance
    from PySide import QtCore
    from PySide import QtGui as QtWidgets

#gets the maya main window
def getMayaWindow():
    mayaWindowptr = omui.MQtUtil.mainWindow()
    window = wrapInstance(long(mayaWindowptr), QtWidgets.QWidget)
    return window 

#this class makes the UI and pins the control     
class pinControlUI(QtWidgets.QMainWindow):
    def __init__(self, parent = getMayaWindow()):
        super(pinControlUI, self).__init__(parent)
        self.makeUI()
        self.show()
        self.connectSignals()

        
    #this function makes a simple UI    
    def makeUI(self):
        #makes the main window 
        self.window = QtWidgets.QWidget()
        self.setWindowTitle('Pin Control')
        self.window.resize(350, 175)
        self.window.setMinimumSize(350, 175)
        self.window.setMaximumSize(350, 175)
        self.verticalWindowLayout = QtWidgets.QVBoxLayout(self.window) 
        
        #makes a frame
        self.frame = QtWidgets.QFrame(self.window)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.verticalFrameLayout = QtWidgets.QVBoxLayout(self.frame)
        
        #makes a label and text box for holding the selected control 
        self.label = QtWidgets.QLabel()
        self.label.setText('Selected Control:')
        self.horizontalCtrlLayout = QtWidgets.QHBoxLayout()
        self.horizontalCtrlLayout.addWidget(self.label)
        self.verticalFrameLayout.addLayout(self.horizontalCtrlLayout)
        
        self.textBox = QtWidgets.QLineEdit()
        #self.textBox.setText(str(self.selected))
        self.textBox.setReadOnly(True)
        self.horizontalCtrlLayout.addWidget(self.textBox)
        
        #makes a button to select a control 
        self.button = QtWidgets.QPushButton()
        self.button.setText('select')
        self.horizontalCtrlLayout.addWidget(self.button)
        
        #makes a line to seperate selecting the control from pinning it 
        self.line = QtWidgets.QFrame()
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.verticalFrameLayout.addWidget(self.line)
        
        #makes a button to execute pinning the control
        self.pinButton = QtWidgets.QPushButton()
        self.pinButton.setText('Pin Control')
        self.pinButton.setMinimumSize(310, 35)
        self.pinButton.setMaximumSize(310, 35)
        self.verticalFrameLayout.addWidget(self.pinButton)
        #makes a dividing line
        self.lowerLine = QtWidgets.QFrame()
        self.lowerLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.lowerLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.verticalFrameLayout.addWidget(self.lowerLine)
        #makes a button for baking down animation layers
        self.bakeButton = QtWidgets.QPushButton()
        self.bakeButton.setText('Bake Animation')
        self.bakeButton.setMinimumSize(310, 35)
        self.bakeButton.setMaximumSize(310, 35)
        self.verticalFrameLayout.addWidget(self.bakeButton)
        
        self.verticalWindowLayout.addWidget(self.frame)
        self.setCentralWidget(self.window)
		
    #connects signals for the UI
    def connectSignals(self):
    	QtCore.QObject.connect(self.button, QtCore.SIGNAL('clicked()'), self.buttonPressed)
    	QtCore.QObject.connect(self.pinButton, QtCore.SIGNAL('clicked()'), self.setKeys)
    	QtCore.QObject.connect(self.bakeButton, QtCore.SIGNAL('clicked()'), self.bakeButtonPressed)
 
    #this function gets the selected control and throws warnings if the selection is invalid 
    def getControl(self):
        #gets a list of selected objects in the scene
        selected = pm.ls(selection = True)
        #checks if the list is empty
        if len(selected) < 1:
            nothingSelectedWarning = QtWidgets.QMessageBox()
            nothingSelectedWarning.setWindowTitle('Warning')
            nothingSelectedWarning.setText('No control selected. Please select one control to continue.')
            nothingSelectedWarning.exec_()
        #checks if there is more than one control selected     
        elif len(selected) > 1:
            tooManyWarning = QtWidgets.QMessageBox()
            tooManyWarning.setWindowTitle('Warning')
            tooManyWarning.setText('More than one object selected. Please select one control to continue.')
            tooManyWarning.exec_() 
        #if only one thing is selected return it     
        else: 
            return selected[0] 
   
    #This function gets the value of keys at a given time on a specified animation curve
    def getKeyValue(self, time, animCurve): 
        pm.currentTime(time, edit = True)
        #this grabs the value of the key at the current frame 
        valueList = pm.keyframe(animCurve, query = True, eval = True)
        return valueList 
    
    #checks that user frame range is within the range of frames on the control 
    def isValid(self):
        valid = True 
        #gets nodes for pin layer
        self.layerNodes =  self.affectingLayers[0].getAnimCurves()
        layerKeyTimesList = pm.keyframe(self.layerNodes[0], query = True, tc = True)
        #finds the first frame that the control is keyed on 
        self.firstFrame = layerKeyTimesList[0]
        #finds the last frame the control is keyed on 
        self.lastFrame = layerKeyTimesList[len(layerKeyTimesList)-1]
        
        #gets nodes for base layer
        self.baseAnimNode = self.affectingLayers[0].getBaseAnimCurves()
        baseKeyTimes = pm.keyframe(self.baseAnimNode[0], query = True, tc = True)
        #finds first frame
        self.baseFirstFrame = baseKeyTimes[0]
        #finds last frame
        self.baseLastFrame = baseKeyTimes[len(baseKeyTimes) -1] 
        
        #checks that frames on pin layer are in range of the first and last frame on base layer
        if self.firstFrame < self.baseFirstFrame or self.lastFrame > self.baseLastFrame:
            timeInvalidWarning = QtWidgets.QMessageBox()
            timeInvalidWarning.setWindowTitle('Warning')
            timeInvalidWarning.setText('Frame range is not valid.')
            timeInvalidWarning.exec_()
            valid = False
        
        return valid  

    def setKeys(self):
        numKeysValid = self.frameNumberCheck()
        #checks to see if frame range is valid 
        valid = self.isValid()
        
        #if the frame range is valid 
        if valid == True and numKeysValid == True:
            #gets the value from the first hold frame 
            self.startValues = self.getKeyValue(self.firstFrame, self.baseAnimNode)
            print self.startValues
            incTime = self.firstFrame
            for key in range(int(self.firstFrame), int(self.lastFrame)):
                incTime += 1.0
                self.currentValues = self.getKeyValue(incTime, self.baseAnimNode)
                print self.currentValues 
                list = []
                #list of possible control attributes
                self.attList = ['visablitiy','translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 'scaleX', 'scaleY', 'scaleZ']
                for v in range(10):
                    print self.startValues[v], self.currentValues[v]
                    value = (self.startValues[v] - self.currentValues[v]) + self.currentValues[v]
                    
                    if value == 0:
                        value = self.startValues[v]
                    list.append(value)
                    pm.setKeyframe(t = int(incTime), al = self.affectingLayers[0], at = self.attList[v], v = value)
               
            #adds a transtion key between end of hold and the rest of the animation     
            self.zeroKey()
         
 
    #sets a zero key five frames after the hold to create a blend     
    def zeroKey(self):
        self.zeroValues = self.getKeyValue(self.lastFrame + 5.0, self.baseAnimNode)
        for v in range(10):
           pm.setKeyframe(t = self.lastFrame + 5.0, al = self.affectingLayers[0], at = self.attList[v], value = self.zeroValues[v])
            
    #this function executes when the selected button is pressed         
    def buttonPressed(self):
        self.selected = self.getControl()
        ctrlName = str(self.selected)
        pm.animLayer(ctrlName + '_1', selected = True, addSelectedObjects = True)
        #gets a list off all layer affecting the current control 
        self.affectingLayers = pm.animLayer(query = True, afl = True)
        #deselects all the affecting layers 
        for layer in self.affectingLayers:
            pm.animLayer(layer, edit = True, selected = False)
        self.affectingLayers[0].setSelected(True)
        
        self.textBox.setText(ctrlName)
    #bakse the animation layers down to the base animation layer
    def bakeButtonPressed(self):
        #gets layers to bake down 
        layerList = [self.affectingLayers[0], self.affectingLayers[len(self.affectingLayers)-1]]
        #bakes down the layer
        pm.bakeResults(t = (self.baseFirstFrame, self.baseLastFrame), rwl = layerList, ral = True)
        #deletes the pin layer
        pm.delete(self.affectingLayers[0])
     
    #checks to make sure the right number of frames are set    
    def frameNumberCheck(self):
        frameNumValid = True 
        #grabs animation nodes
        nodes =  self.affectingLayers[0].getAnimCurves()
        #if there are animation nodes
        if nodes:
            #gets the number of keys 
            numKeys = pm.keyframe(nodes[0], query = True, keyframeCount = True)
            if numKeys < 2:
                oneKeyWarning = QtWidgets.QMessageBox()
                oneKeyWarning.setWindowTitle('Warning')
                oneKeyWarning.setText('Only one key set. Please set two keys to continue.')
                oneKeyWarning.exec_()
                frameNumValid = False
                
            elif numKeys > 2:
                manyKeysWarning = QtWidgets.QMessageBox()
                manyKeysWarning.setWindowTitle('Warning')
                manyKeysWarning.setText('Too many keys set. Please set two keys to continue')
                manyKeysWarning.exec_()
                frameNumValid = False 
        #if there are no animation nodes tells user to set keys 
        else:
            noKeysWarning = QtWidgets.QMessageBox()
            noKeysWarning.setWindowTitle('Warning')
            noKeysWarning.setText('No keys set. Please set two keys to continue.')
            noKeysWarning.exec_()
            frameNumValid = False 
        return frameNumValid
        
test = pinControlUI()