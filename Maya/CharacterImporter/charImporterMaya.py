from PySide2 import QtGui, QtCore, QtWidgets
import maya.OpenMayaUI as omui 
from shiboken2 import wrapInstance
import os 
import pymel.core as pm 

#Finds the main maya window 
def getMayaWindow():
    mayaWindowptr = omui.MQtUtil.mainWindow()
    window = wrapInstance(long(mayaWindowptr), QtWidgets.QWidget)
    return window
    
    
'''
class used to setup the UI and functions for a character importer
'''   
class charImporterUI(QtWidgets.QMainWindow):
    def __init__(self, parent = getMayaWindow()):
        super(charImporterUI, self).__init__(parent)
        
        self.makeCharImporterUI()
        self.connectSignals()
        self.show()
   
    #sets up the signals for the UI reacting to user input    
    def connectSignals(self):
        QtCore.QObject.connect(self.prjDropdown, QtCore.SIGNAL('activated(QString)'), self.setupCharDropdown)
        QtCore.QObject.connect(self.importButton, QtCore.SIGNAL('clicked()'), self.importChar)
    
    #makes the UI    
    def makeCharImporterUI(self):
        #creates base window
        self.setWindowTitle('Character Importer')
        self.window = QtWidgets.QWidget()
        self.window.resize(500,200)
        self.window.setMinimumSize(500,200)
        self.window.setMaximumSize(500,200)
        self.verticalWindowLayout = QtWidgets.QVBoxLayout(self.window)
        
        #makes a frame
        self.frame = QtWidgets.QFrame(self.window)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.verticalFrameLayout = QtWidgets.QVBoxLayout(self.frame)
        
        #adds a label to the top of the UI
        self.label = QtWidgets.QLabel()
        self.label.setText('<b>Select Character :</b>')
        self.verticalFrameLayout.addWidget(self.label)
        
        self.horizontalDropdownLayout = QtWidgets.QHBoxLayout()
        self.verticalFrameLayout.addLayout(self.horizontalDropdownLayout)
        
        #sets up the first dropdown menu
        self.prjLabel = QtWidgets.QLabel()
        self.prjLabel.setText('Project:')
        self.horizontalDropdownLayout.addWidget(self.prjLabel)
        self.prjDropdown = QtWidgets.QComboBox()
        self.prjDropdown.setMinimumSize(150,22)
        self.prjDropdown.setMaximumSize(150,22)
        self.horizontalDropdownLayout.addWidget(self.prjDropdown)
        
        #adds items to dropdown
        self.path = 'N:\Art\mocap\skeletons\characters'
        folders = os.listdir(self.path)
        for f in folders:
            self.prjDropdown.addItem(f)
        
        
        self.spacerDropdowns = QtWidgets.QSpacerItem(40,20)
        self.horizontalDropdownLayout.addItem(self.spacerDropdowns)
        
        #sets up the second dropdown menu
        self.charLabel = QtWidgets.QLabel()
        self.charLabel.setText('Character:')
        self.horizontalDropdownLayout.addWidget(self.charLabel)
        self.charDropdown = QtWidgets.QComboBox()
        self.horizontalDropdownLayout.addWidget(self.charDropdown)
        self.charDropdown.setMinimumSize(150,22)
        self.charDropdown.setMaximumSize(150,22)
        self.spacerCharMenu = QtWidgets.QSpacerItem(15,15)
        self.horizontalDropdownLayout.addItem(self.spacerCharMenu)
        
        
        #adds items to second dropdown based off the intial state of the first dropdown
        self.pathChar = self.path + '\\' + self.prjDropdown.currentText()
        intialChars = os.listdir(self.pathChar)
        for c in intialChars:
            #filters out non-fbx files and folders
            if c.endswith('.fbx') == True:
                self.charDropdown.addItem(c)
                
        
            
        
        self.spacerDropdownsBottom = QtWidgets.QSpacerItem(10,10)
        self.verticalFrameLayout.addItem(self.spacerDropdownsBottom)
        
        #adds line above namespace
        self.topLine = QtWidgets.QFrame()
        self.topLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.topLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.verticalFrameLayout.addWidget(self.topLine)
        
        self.horizontalNamespaceLayout = QtWidgets.QHBoxLayout()
        self.verticalFrameLayout.addLayout(self.horizontalNamespaceLayout)
       
        #adds line bellow namespace
        self.bottomLine = QtWidgets.QFrame()
        self.bottomLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.bottomLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.verticalFrameLayout.addWidget(self.bottomLine)
        
        #adds a checkbox to the UI
        self.checkbox = QtWidgets.QCheckBox()
        self.horizontalNamespaceLayout.addWidget(self.checkbox)
        self.checkbox.stateChanged.connect(self.enable)
        self.checkboxSpacer = QtWidgets.QSpacerItem(10,20)
        self.horizontalNamespaceLayout.addItem(self.checkboxSpacer)
        
        self.spacerNamespace = QtWidgets.QSpacerItem(5,5)
        self.verticalFrameLayout.addItem(self.spacerNamespace)
        
        #adds the label and line edit for the namespace
        self.nameLabel = QtWidgets.QLabel()
        self.nameLabel.setText('Namespace:')
        self.horizontalNamespaceLayout.addWidget(self.nameLabel)
        self.nameLabel.setDisabled(True)
        
        self.textBox = QtWidgets.QLineEdit()
        self.textBox.setMinimumSize(350,22)
        self.textBox.setMaximumSize(350,22)
        self.horizontalNamespaceLayout.addWidget(self.textBox)
        self.spacerText = QtWidgets.QSpacerItem(15,15)
        self.horizontalNamespaceLayout.addItem(self.spacerText)
       
        #adds a validator to limit possible inputs into the LineEdit
        v = QtCore.QRegExp('[A-Z|a-z|_]\w+')
        self.validator = QtGui.QRegExpValidator(v)
        self.textBox.setValidator(self.validator)
        self.textBox.setDisabled(True)
        
        self.importButton = QtWidgets.QPushButton()
        self.importButton.setText('Import Character')
        self.importButton.setMinimumSize(460,30)
        self.importButton.setMaximumSize(460,30)
        self.verticalFrameLayout.addWidget(self.importButton)
        
        self.verticalWindowLayout.addWidget(self.frame)
        self.setCentralWidget(self.window)
    
    #enables/disables parts of the UI based off the state of the checkbox    
    def enable(self):
        if (self.checkbox.isChecked() == True):
            self.textBox.setDisabled(False)
            self.nameLabel.setDisabled(False)
            
        else:
            self.textBox.setDisabled(True)
            self.nameLabel.setDisabled(True)
    #changes the contents of the second dropbox based off the folder selected by the first dropbox    
    def setupCharDropdown(self):
        self.charDropdown.clear()
        path = self.path + '\\' + self.prjDropdown.currentText()
        files = os.listdir(path)
       
        for f in files:
            if f.endswith('.fbx') == True:
                self.charDropdown.addItem(f) 
    
    #imports character when button is pressed           
    def importChar(self):
        importFile = self.path + '\\' + self.prjDropdown.currentText() + '\\' + self.charDropdown.currentText()
        
		#if the user set a namespace and the namespace doesn't exist in maya reference the character
		if self.checkbox.isChecked() == True and (pm.namespace(exists = self.textBox.text()) == False):
           pm.createReference(importFile, namespace = self.textBox.text())
       
   	    #if the user did not set a namespace check if character is already in the scene    
        elif self.checkbox.isChecked() == False:
           
            charExists = False 
            #gets list of referecned nodes 
            list = pm.ls(rf = True)
            #gets charater name from character dropdown menu
            fileName = self.charDropdown.currentText()
            #removes .fbx and adds RN for reference name 
            charName = fileName[0:(len(fileName)-4)] +'RN'
          
            #compares references to character name 
            for node in list:
                #if the character is in the scene it marks character Exists as true 
                if charName == node: 
                    charExists = True
                    break
					
            #if the character exists give the user a warning           
            if charExists == True:
                charExistsWarning = QtWidgets.QMessageBox()
                charExistsWarning.setWindowTitle('Warning')
                charExistsWarning.setText('This character is already in the scene. Please add a namespace to import.')
                charExistsWarning.exec_()
				
            #if the character doesn't exist refrence the character    
            else:
               pm.createReference(importFile)
			   
        #if the users set a namespace and the namespace exists in maya give the user a warning    
        else: 
           
            namespaceWarning = QtWidgets.QMessageBox()
            namespaceWarning.setWindowTitle('Warning')
            namespaceWarning.setText('This namespace is already in use. Please change namespace to import.')
            namespaceWarning.exec_()
          
               
charImporterUI()