'''
This script is a character importer. It has a class in it that sets up the UI and 
functions.
It contains these functions:
-connectSignals()
-makeCharImporterUI()
-enable()
-setupCharDropdown()
-warningsCheck()
-importChar()
'''
#-------------------
#imports
#-------------------
from PySide import QtGui, QtCore
import os
from pyfbsdk import *
import MBUtils as utils

#------------------
#global varibles
#------------------
FILEPATH = 'N:\Art\mocap\skeletons\characters'

'''
class used to setup the UI and functions for a character importer
'''
class charImporterUI(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(charImporterUI, self).__init__(parent)
        
        self.makeCharImporterUI()
        self.connectSignals()
        utils.populateDropdown(self.prjDropdown, FILEPATH)
        self.setupCharDropdown()
        self.enable()
        self.app = FBApplication()

        self.show()
    #sets up the signals for the UI reacting to user input    
    def connectSignals(self):
        QtCore.QObject.connect(self.prjDropdown, QtCore.SIGNAL('activated(QString)'), self.setupCharDropdown)
        QtCore.QObject.connect(self.importButton, QtCore.SIGNAL('clicked()'), self.importChar)
        QtCore.QObject.connect(self.checkbox, QtCore.SIGNAL('stateChanged(int)'), self.enable)
      
    #makes the UI    
    def makeCharImporterUI(self):
        
        #creates base window
        self.window = QtGui.QWidget()
        self.setWindowTitle('Character Importer')
        self.resize(500, 200)
        self.setMinimumSize(500,200)
        self.setMaximumSize(500,200)
        self.verticalWindowLayout = QtGui.QVBoxLayout(self.window)
       
        #makes a frame
        self.frame = QtGui.QFrame(self.window)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.verticalFrameLayout = QtGui.QVBoxLayout(self.frame)
        
        #adds a label to the top of the UI
        self.label = QtGui.QLabel()
        self.label.setText("<b>Select Character :</b>")
        self.verticalFrameLayout.addWidget(self.label)

              
        self.horizontalDropdownLayout = QtGui.QHBoxLayout()
        self.verticalFrameLayout.addLayout(self.horizontalDropdownLayout)
       
        #sets up the first dropdown menu
        self.prjLabel = QtGui.QLabel()
        self.prjLabel.setText('Project:')
        self.horizontalDropdownLayout.addWidget(self.prjLabel)
        self.prjDropdown = QtGui.QComboBox()
        self.prjDropdown.setMinimumSize(150,22)
        self.prjDropdown.setMaximumSize(150,22)
        self.horizontalDropdownLayout.addWidget(self.prjDropdown)  
       
        self.spacerDropdowns = QtGui.QSpacerItem(40,20)
        self.horizontalDropdownLayout.addItem(self.spacerDropdowns)
        
        #sets up the second dropdown menu 
        self.charLabel = QtGui.QLabel()
        self.charLabel.setText('Character:')
        self.horizontalDropdownLayout.addWidget(self.charLabel)
        self.charDropdown = QtGui.QComboBox()
        self.horizontalDropdownLayout.addWidget(self.charDropdown)
        self.charDropdown.setMinimumSize(150,22)
        self.charDropdown.setMaximumSize(150,22)
        self.spacerCharMenu = QtGui.QSpacerItem(15,15)
        self.horizontalDropdownLayout.addItem(self.spacerCharMenu)         
            
        self.spacerDropdownsButtom = QtGui.QSpacerItem(10, 10)
        self.verticalFrameLayout.addItem(self.spacerDropdownsButtom)
        
        #adds line above namespace
        self.topLine = QtGui.QFrame()
        self.topLine.setFrameShape(QtGui.QFrame.HLine)
        self.topLine.setFrameShadow(QtGui.QFrame.Sunken)
        self.verticalFrameLayout.addWidget(self.topLine)
    
        self.horizontalNamespaceLayout = QtGui.QHBoxLayout()
        self.verticalFrameLayout.addLayout(self.horizontalNamespaceLayout)
        
        #adds line bellow namespace
        self.bottomLine = QtGui.QFrame()
        self.bottomLine.setFrameShape(QtGui.QFrame.HLine)
        self.bottomLine.setFrameShadow(QtGui.QFrame.Sunken)
        self.verticalFrameLayout.addWidget(self.bottomLine)
        
        #adds a checkbox to the UI
        self.checkbox = QtGui.QCheckBox()
        self.horizontalNamespaceLayout.addWidget(self.checkbox)
        self.checkboxSpacer = QtGui.QSpacerItem(10,20)
        self.horizontalNamespaceLayout.addItem(self.checkboxSpacer)
        
        self.spacerNamespace = QtGui.QSpacerItem(5, 5)
        self.verticalFrameLayout.addItem(self.spacerNamespace)
       
        #adds the label and line edit for the namespace
        self.nameLabel = QtGui.QLabel()
        self.nameLabel.setText('Namespace:')
        self.horizontalNamespaceLayout.addWidget(self.nameLabel)
        
        self.textField = QtGui.QLineEdit()
        self.textField.setMinimumSize(350,22)
        self.textField.setMaximumSize(350,22)
        self.horizontalNamespaceLayout.addWidget(self.textField)
        self.spacerText = QtGui.QSpacerItem(15,15)
        self.horizontalNamespaceLayout.addItem(self.spacerText)
      
        #adds a validator to limit possible inputs into the LineEdit
        v = QtCore.QRegExp('[A-Z|a-z|_]\w+')
        self.validator = QtGui.QRegExpValidator(v)
        self.textField.setValidator(self.validator)
        
        #adds button to import character
        self.importButton = QtGui.QPushButton()
        self.importButton.setText('Import Character')
        self.importButton.setMinimumSize(460,30)
        self.importButton.setMaximumSize(460,30)
        self.verticalFrameLayout.addWidget(self.importButton)
        
       
        self.verticalWindowLayout.addWidget(self.frame)
    
       
        self.setCentralWidget(self.window)

    #enables/disables parts of the UI based off the state of the checkbox
    def enable(self):
        if self.checkbox.isChecked() == True:
            self.textField.setDisabled(False)
            self.nameLabel.setDisabled(False)
       
        else:
            self.textField.setDisabled(True)
            self.nameLabel.setDisabled(True)
            
    #changes the contents of the second dropbox based off the folder selected by the first dropbox    
    def setupCharDropdown(self):

        self.charDropdown.clear()
        path = FILEPATH + '\\' + self.prjDropdown.currentText()
        files = os.listdir(path)
        for f in files:
            if f.endswith('.fbx') == True:
                self.charDropdown.addItem(f)
                
    #this function checks if character or namespace is already in use before importing     
    def warningsCheck(self):
        warning = False
        if self.checkbox.isChecked() == True:
            #checks scene for the namespace
            namespace = str(self.textField.text())
            searchName = str(self.textField.text() + ':*')
            foundCharacters = utils.findObjects(searchName)                  
            
            #if nothing was found using that namespace import the character with the namespace
            if len(foundCharacters) > 0:
                namespaceWarning = QtGui.QMessageBox()
                namespaceWarning.setWindowTitle('Warning')
                namespaceWarning.setText('This namespace is already in use. Please change namespace to import.')
                namespaceWarning.exec_()
                warning = True 
                return warning
                
        #if no namespace is set 
        elif self.checkbox.isChecked() == False:
            #gets the name of the character
            fileName = str(self.charDropdown.currentText())
            #removes _skel.fbx from the character name 
            charName = utils.shortenString(fileName, 9)
            #looks for uses of the character name in the scene 
            foundCharacters = utils.findObjects(charName)
            charExists = False
            
            #checks to see if there is a motionbuilder character with the given name in the list
            for char in foundCharacters:
                if str(char.FullName) == str('Constraint::' + charName):
                    charExists = True
                    break
                    
            #if no character was found imports the character
            if charExists == True:
                charExistsWarning = QtGui.QMessageBox()
                charExistsWarning.setWindowTitle('Warning')
                charExistsWarning.setText('This character is already in the scene. Please add a namespace to import')
                charExistsWarning.exec_()
                warning = True
                return warning 
        return warning 
    
    #imports character when button is pressed if no warnings were issued            
    def importChar(self):
        self.importFile = str(FILEPATH + '\\' + self.prjDropdown.currentText() + '\\' + self.charDropdown.currentText())
        namespace = None
        warningState = self.warningsCheck()
        print warningState
        if warningState == False: 
            #if the user set a namespace
            if self.checkbox.isChecked() == True:
                #checks scene for the namespace
                namespace = str(self.textField.text())
                    
            utils.mergeCharacter(namespace, self.importFile, self.app)
     
        
#test = charImporterUI()