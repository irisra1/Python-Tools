'''
This script is for making a control rig based off user input.
It contains these functions:
    - getMayaWindow()
    - makeUI()
    - connectSignals()
    - makeTitleLabel(label, page)
    - makeLine(page)
    - populateJointDropdowns()
    - findJoints()
    - duplicateJoints(jointList, prefix)
    - makeIK(ctrlType)
    - parentObject(parentObject, childObject)
    - parentConstrainObject(parent, child)
    - makeCtrl(radius, name, ctrlType)
    - getSetPostion(radius, name, joint, ctrlType)
    - makeFKCtrl(skJoint, fkJoint, name, ctrlType)
    - makeFKChain(ctrlType)
    - makeIkFkSwitchCtrl(name, ctrlType)
    - ikFkSwitch(fkJoint, IkJoint, skJoint)
    - makeCtrlSkeleton()
    - findCtrlJoint(skJoint)
    - makeCtrls()
    - makeWorldCtrl()
    - parentWorld()
    - makeCog()
    - getSelectedParentControl()
    - getSelectedChildControl()
    - parentCtrls()
    - enable()
    - getJoint(dropDown)
'''
#------------------
#Imports
#------------------
import pymel.core as pm 
import maya.OpenMayaUI as omui

#this makes the tool compatible with both 2014 and 2018
try:
    from PySide2 import QtGui, QtCore, QtWidgets
    from shiboken2 import wrapInstance

except:
    from shiboken import wrapInstance
    from PySide import QtCore
    from PySide import QtGui as QtWidgets 
    
#------------------
#General Functions
#------------------

#gets the main maya window
def getMayaWindow():
    mayaWindowptr = omui.MQtUtil.mainWindow()
    window = wrapInstance(long(mayaWindowptr), QtWidgets.QWidget)
    return window 
    
#------------------
#Class
#------------------

class ctrlRigUI(QtWidgets.QMainWindow):
    def __init__(self, parent = getMayaWindow()):
        super(ctrlRigUI, self).__init__(parent)
        self.makeUI()
        self.populateJointDropdowns()
        self.enable()
        self.connectSignals()
        self.show()
    
    def makeUI(self):
        #list to keep track of dropdowns created
        self.dropdownList = []
        #makes the main window
        self.window = QtWidgets.QWidget()
        self.setWindowTitle('Make Control Rig')
        self.window.resize(600, 550)
        self.window.setMaximumSize(600, 620)
        self.window.setMinimumSize(600, 620)
        self.verticalWindowLayout = QtWidgets.QVBoxLayout(self.window)
        
        #makes a frame
        self.frame = QtWidgets.QFrame(self.window)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.verticalFrameLayout = QtWidgets.QHBoxLayout(self.frame)
        self.verticalWindowLayout.addWidget(self.frame)

        self.verticalMidLayout = QtWidgets.QVBoxLayout()
        self.verticalFrameLayout.addLayout(self.verticalMidLayout)

        #make control
        self.makeLine(self.verticalMidLayout)
        self.makeTitleLabel('Make Controls', self.verticalMidLayout)
        self.makeLine(self.verticalMidLayout)
        
        self.spacer6 = QtWidgets.QSpacerItem(480, 10)
        self.verticalMidLayout.addItem(self.spacer6) 
        
        #control type
        self.ctrlTypeHorizontalLayout = QtWidgets.QHBoxLayout()
        self.verticalMidLayout.addLayout(self.ctrlTypeHorizontalLayout)
        
        #makes a label for the control type row
        self.ctrlTypeLabel = QtWidgets.QLabel()
        self.ctrlTypeLabel.setText('Control Type:')
        self.ctrlTypeHorizontalLayout.addWidget(self.ctrlTypeLabel)
        
        self.spacer10 = QtWidgets.QSpacerItem(40, 10)
        self.ctrlTypeHorizontalLayout.addItem(self.spacer10)
        
        #makes a button group to contain the control type buttons
        self.ctrlTypeButtonGroup = QtWidgets.QButtonGroup()
        
        #makes a fk button and label
        self.fkButton = QtWidgets.QRadioButton()
        self.ctrlTypeButtonGroup.addButton(self.fkButton) 
        self.ctrlTypeHorizontalLayout.addWidget(self.fkButton)
        self.fkLabel = QtWidgets.QLabel()
        self.fkLabel.setText('FK')
        self.ctrlTypeHorizontalLayout.addWidget(self.fkLabel)
        self.spacer11 = QtWidgets.QSpacerItem(40, 10)
        self.ctrlTypeHorizontalLayout.addItem(self.spacer11)
        
        #makes an ik button and label
        self.ikButton = QtWidgets.QRadioButton()
        self.ctrlTypeButtonGroup.addButton(self.ikButton) 
        self.ctrlTypeHorizontalLayout.addWidget(self.ikButton)
        self.ikLabel = QtWidgets.QLabel()
        self.ikLabel.setText('IK')
        self.ctrlTypeHorizontalLayout.addWidget(self.ikLabel)
        self.spacer12 = QtWidgets.QSpacerItem(40, 10)
        self.ctrlTypeHorizontalLayout.addItem(self.spacer12)
        
        #makes an ik/fk button and label
        self.ikFkButton = QtWidgets.QRadioButton()
        self.ctrlTypeButtonGroup.addButton(self.ikFkButton) 
        self.ctrlTypeHorizontalLayout.addWidget(self.ikFkButton)
        self.ikFkLabel = QtWidgets.QLabel()
        self.ikFkLabel.setText('IK/FK')
        self.ctrlTypeHorizontalLayout.addWidget(self.ikFkLabel)
        self.spacer13 = QtWidgets.QSpacerItem(120, 10)
        self.ctrlTypeHorizontalLayout.addItem(self.spacer13)
        
        #ctrl location 
        self.ctrlLocationHorizontalLayout = QtWidgets.QHBoxLayout()
        self.verticalMidLayout.addLayout(self.ctrlLocationHorizontalLayout)
        self.ctrlLocationLabel = QtWidgets.QLabel()
        
        #makes a label for the control location row
        self.ctrlLocationLabel.setText('Control Location:')
        self.ctrlLocationHorizontalLayout.addWidget(self.ctrlLocationLabel)
        
        self.spacerCtrlLoc = QtWidgets.QSpacerItem(20, 10)
        self.ctrlLocationHorizontalLayout.addItem(self.spacerCtrlLoc)
        
        #makes a button group to contain all the control location buttons
        self.ctrlLocationButtonGroup = QtWidgets.QButtonGroup()
        
        #makes a middle button and label
        self.midButton = QtWidgets.QRadioButton()
        self.ctrlLocationButtonGroup.addButton(self.midButton)
        self.ctrlLocationHorizontalLayout.addWidget(self.midButton)
        self.midLabel = QtWidgets.QLabel()
        self.midLabel.setText('Middle')
        self.ctrlLocationHorizontalLayout.addWidget(self.midLabel)
        
        self.spacerCtrlLoc1 = QtWidgets.QSpacerItem(30, 10)
        self.ctrlLocationHorizontalLayout.addItem(self.spacerCtrlLoc1)
        
        #makes a right button and label
        self.rightButton = QtWidgets.QRadioButton()
        self.ctrlLocationButtonGroup.addButton(self.rightButton)
        self.ctrlLocationHorizontalLayout.addWidget(self.rightButton)
        self.rightLabel = QtWidgets.QLabel()
        self.rightLabel.setText('Right')
        self.ctrlLocationHorizontalLayout.addWidget(self.rightLabel)
        
        self.spacer2CtrlLoc = QtWidgets.QSpacerItem(30, 10)
        self.ctrlLocationHorizontalLayout.addItem(self.spacer2CtrlLoc)
        
        #makes a left button and label
        self.leftButton = QtWidgets.QRadioButton()
        self.ctrlLocationButtonGroup.addButton(self.leftButton)
        self.ctrlLocationHorizontalLayout.addWidget(self.leftButton)
        self.leftLabel = QtWidgets.QLabel()
        self.leftLabel.setText('Left')
        self.ctrlLocationHorizontalLayout.addWidget(self.leftLabel)
        
        self.spacer3CtrlLoc = QtWidgets.QSpacerItem(30, 10)
        self.ctrlLocationHorizontalLayout.addItem(self.spacer3CtrlLoc)
        
        #makes an extra button and label 
        self.extraButton = QtWidgets.QRadioButton()
        self.ctrlLocationButtonGroup.addButton(self.extraButton)
        self.ctrlLocationHorizontalLayout.addWidget(self.extraButton)
        self.extraLabel = QtWidgets.QLabel()
        self.extraLabel.setText('Extra')
        self.ctrlLocationHorizontalLayout.addWidget(self.extraLabel)
        
        self.spacer4CtrlLoc = QtWidgets.QSpacerItem(30, 10)
        self.ctrlLocationHorizontalLayout.addItem(self.spacer4CtrlLoc)

        #Makes dropdowns for start and end Joints
        self.spacer5 = QtWidgets.QSpacerItem(480, 10)
        self.verticalMidLayout.addItem(self.spacer5) 
        
        self.jointDropdownHorizontalLayout = QtWidgets.QHBoxLayout()
        self.verticalMidLayout.addLayout(self.jointDropdownHorizontalLayout)
        self.jointStartLabel = QtWidgets.QLabel()
        self.jointStartLabel.setText('Start Joint:')
        self.jointDropdownHorizontalLayout.addWidget(self.jointStartLabel)
        self.Dropdown1 = QtWidgets.QComboBox()
        self.Dropdown1.setMaximumSize(180, 20)
        self.Dropdown1.setMinimumSize(180, 20)
        self.jointDropdownHorizontalLayout.addWidget(self.Dropdown1)
        self.dropdownList.append(self.Dropdown1)
        
        self.spacer8 = QtWidgets.QSpacerItem(40, 10)
        self.jointDropdownHorizontalLayout.addItem(self.spacer8)
        
        self.jointEndLabel = QtWidgets.QLabel()
        self.jointEndLabel.setText('End Joint:')
        self.jointDropdownHorizontalLayout.addWidget(self.jointEndLabel)
        self.Dropdown2 = QtWidgets.QComboBox()
        self.Dropdown2.setMaximumSize(180, 20)
        self.Dropdown2.setMinimumSize(180, 20)
        self.jointDropdownHorizontalLayout.addWidget(self.Dropdown2)
        self.dropdownList.append(self.Dropdown2)
        
        #makes a dropdown for middle joint to be used in pole vector placement 
        self.midJointHorizontalLayout = QtWidgets.QHBoxLayout()
        self.verticalMidLayout.addLayout(self.midJointHorizontalLayout)
        self.midJointLabel = QtWidgets.QLabel()
        self.midJointLabel.setText('Middle Joint:')
        self.midJointHorizontalLayout.addWidget(self.midJointLabel)
        self.midJointDropdown = QtWidgets.QComboBox()
        self.midJointDropdown.setMaximumSize(180, 20)
        self.midJointDropdown.setMinimumSize(180, 20)
        self.midJointHorizontalLayout.addWidget(self.midJointDropdown)
        self.dropdownList.append(self.midJointDropdown)
        self.middleSpacer = QtWidgets.QSpacerItem(300, 20)
        self.midJointHorizontalLayout.addItem(self.middleSpacer)
        
        self.polevectorHorizontalLayout = QtWidgets.QHBoxLayout()
        self.verticalMidLayout.addLayout(self.polevectorHorizontalLayout)
        
        #makes a label for the pole vector postion row
        self.polevectorLabel = QtWidgets.QLabel()
        self.polevectorLabel.setText('Pole Vector Postion:')
        self.polevectorHorizontalLayout.addWidget(self.polevectorLabel)
        self.polevectorSpacer = QtWidgets.QSpacerItem(20,20)
        self.polevectorHorizontalLayout.addItem(self.polevectorSpacer)
        
        #makes a group for the pole vector postion buttons
        self.postionButtonGroup = QtWidgets.QButtonGroup()
        
        #makes a button and label for placing the pole vector in front of the moddel
        self.frontButton = QtWidgets.QRadioButton()
        self.postionButtonGroup.addButton(self.frontButton)
        self.polevectorHorizontalLayout.addWidget(self.frontButton)
        self.frontLabel = QtWidgets.QLabel()
        self.frontLabel.setText('Front')
        self.polevectorHorizontalLayout.addWidget(self.frontLabel)
        
        #makes a button and label for placing the pole vector behind the moddel
        self.backButton = QtWidgets.QRadioButton()
        self.postionButtonGroup.addButton(self.backButton)
        self.polevectorHorizontalLayout.addWidget(self.backButton)
        self.backLabel = QtWidgets.QLabel()
        self.backLabel.setText('Back')
        self.polevectorHorizontalLayout.addWidget(self.backLabel)
        
        #makes a button and label for placing the pole vector to the right of the moddel
        self.rightButton2 = QtWidgets.QRadioButton()
        self.postionButtonGroup.addButton(self.rightButton2)
        self.polevectorHorizontalLayout.addWidget(self.rightButton2)
        self.rightLabel2 = QtWidgets.QLabel()
        self.rightLabel2.setText('Right')
        self.polevectorHorizontalLayout.addWidget(self.rightLabel2)
        
        #makes a button and label for placing the pole vector to the left of the moddel
        self.leftButton2 = QtWidgets.QRadioButton()
        self.postionButtonGroup.addButton(self.leftButton2)
        self.polevectorHorizontalLayout.addWidget(self.leftButton2)
        self.leftLabel2 = QtWidgets.QLabel()
        self.leftLabel2.setText('Left')
        self.polevectorHorizontalLayout.addWidget(self.leftLabel2)
        
        #makes a label and a text box for control scale 
        self.scaleFactorHorizontalLayout = QtWidgets.QHBoxLayout()
        self.verticalMidLayout.addLayout(self.scaleFactorHorizontalLayout)
        self.scaleFactorLabel = QtWidgets.QLabel()
        self.scaleFactorLabel.setText('Control Scale:')
        self.scaleFactorHorizontalLayout.addWidget(self.scaleFactorLabel)
        self.scaleFactorTextBox = QtWidgets.QLineEdit()
        self.scaleFactorTextBox.setMinimumSize(100, 20)
        self.scaleFactorTextBox.setMaximumSize(100, 20)
        self.scaleFactorTextBox.setText('1.0')
        
        #makes a validator for the control scale text box to insure only numbers and decimal points are valid inputs 
        self.validatorSettings = QtCore.QRegExp('[0-9.]+')
        self.scaleValidator = QtGui.QRegExpValidator(self.validatorSettings)
        self.scaleFactorTextBox.setValidator(self.scaleValidator)
        self.scaleFactorHorizontalLayout.addWidget(self.scaleFactorTextBox)
        self.scaleFactorSpacer = QtWidgets.QSpacerItem(400, 20)
        self.scaleFactorHorizontalLayout.addItem(self.scaleFactorSpacer)
        
        
        self.spacer9 = QtWidgets.QSpacerItem(40, 10)
        self.jointDropdownHorizontalLayout.addItem(self.spacer9)
        
        #makes the button for making controls
        self.ctrlButton = QtWidgets.QPushButton()
        self.ctrlButton.setText('Make Controls') 
        self.ctrlButton.setMinimumSize(560, 40)
        self.ctrlButton.setMaximumSize(560, 40)
        self.verticalMidLayout.addWidget(self.ctrlButton)
        
        #assemble rig 
        self.makeLine(self.verticalMidLayout)
        self.makeTitleLabel('Assemble Rig', self.verticalMidLayout)
        self.makeLine(self.verticalMidLayout)
        
        #makes a label for the world control 
        self.worldCtrlLabel = QtWidgets.QLabel()
        self.worldCtrlLabel.setText('World Control')
        self.verticalMidLayout.addWidget(self.worldCtrlLabel)
        
        self.worldCtrlHorizontalLayout = QtWidgets.QHBoxLayout()
        self.verticalMidLayout.addLayout(self.worldCtrlHorizontalLayout)
        
        #makes a label for the world control scale 
        self.worldScaleLabel = QtWidgets.QLabel()
        self.worldScaleLabel.setText('Control Scale:')
        self.worldCtrlHorizontalLayout.addWidget(self.worldScaleLabel)
        
        #makes a text box for the scale of the world control 
        self.worldScaleTextBox = QtWidgets.QLineEdit()
        self.worldScaleTextBox.setMinimumSize(100,20)
        self.worldScaleTextBox.setMaximumSize(100, 20)
        self.worldScaleTextBox.setText('1.0')
        
        #makes a validator to insure only numbers and decimal points are valid inputs
        self.scaleWorldValidator = QtGui.QRegExpValidator(self.validatorSettings)
        self.worldScaleTextBox.setValidator(self.scaleWorldValidator)
        self.worldCtrlHorizontalLayout.addWidget(self.worldScaleTextBox)
        
        #makes a button for creating the world control 
        self.worldCtrlButton = QtWidgets.QPushButton()
        self.worldCtrlButton.setText('Make World Control')
        self.worldCtrlHorizontalLayout.addWidget(self.worldCtrlButton)
        
        #makes a button for parenting all the controls and control joints under the world control 
        self.worldParentButton = QtWidgets.QPushButton()
        self.worldParentButton.setText('Parent All Controls to World Control')
        self.worldCtrlHorizontalLayout.addWidget(self.worldParentButton)
        self.spacerWorld = QtWidgets.QSpacerItem(10, 10)
        self.worldCtrlHorizontalLayout.addItem(self.spacerWorld)
        
        self.worldSpacer1 = QtWidgets.QSpacerItem(40, 20)
        self.worldCtrlHorizontalLayout.addItem(self.worldSpacer1)
        
        self.worldCogSpacer = QtWidgets.QSpacerItem(10, 15)
        self.verticalMidLayout.addItem(self.worldCogSpacer)
         
        #makes a label for the cog 
        self.cogLabel = QtWidgets.QLabel()
        self.cogLabel.setText('COG Control')
        self.cogScaleLabel = QtWidgets.QLabel()
        self.verticalMidLayout.addWidget(self.cogLabel)
        
        self.cogHorizontalLayout = QtWidgets.QHBoxLayout()
        self.verticalMidLayout.addLayout(self.cogHorizontalLayout)
                        
        #makes a label for the scale of the cog control
        self.cogScaleLabel.setText('Control Scale:')
        self.cogHorizontalLayout.addWidget(self.cogScaleLabel)
        
        #makes a text box to hold the scale factor for the cog  
        self.cogScaleTextBox = QtWidgets.QLineEdit()
        self.cogScaleTextBox.setMinimumSize(100, 20)
        self.cogScaleTextBox.setMaximumSize(100, 20)
        self.cogScaleTextBox.setText('1.0')
        
        #makes a validator to limit valid inputs to numbers and decimal points 
        self.scaleCogValidator = QtGui.QRegExpValidator(self.validatorSettings)
        self.cogScaleTextBox.setValidator(self.scaleCogValidator)
        
        self.cogHorizontalLayout.addWidget(self.cogScaleTextBox)
        #makes a label for the cog joint dropdown 
        self.cogDropdownLabel = QtWidgets.QLabel()
        self.cogDropdownLabel.setText('Cog Joint:')
        self.cogHorizontalLayout.addWidget(self.cogDropdownLabel)
        
        #makes a dropdown menu for the cog joint
        self.cogDropdown = QtWidgets.QComboBox()
        self.cogDropdown.setMaximumSize(180, 20)
        self.cogDropdown.setMinimumSize(180, 20)
        self.cogHorizontalLayout.addWidget(self.cogDropdown)
        self.dropdownList.append(self.cogDropdown)
        
        #makes a button for creating the cog control
        self.cogButton = QtWidgets.QPushButton()
        self.cogButton.setText('Make COG Control')
        self.cogHorizontalLayout.addWidget(self.cogButton)
        self.spacerCog = QtWidgets.QSpacerItem(20, 10)
        self.cogHorizontalLayout.addItem(self.spacerCog)
        
        self.cogParentSpacer = QtWidgets.QSpacerItem(10, 15)
        self.verticalMidLayout.addItem(self.cogParentSpacer)
        
        #makes a label for the parent control section of the UI
        self.parentCtrlLabel = QtWidgets.QLabel()
        self.parentCtrlLabel.setText('Parent Controls')
        self.verticalMidLayout.addWidget(self.parentCtrlLabel)
        self.makeLine(self.verticalMidLayout)
        
        #makes a label for the parent control 
        self.parentControlHorizontalLayout = QtWidgets.QHBoxLayout()
        self.verticalMidLayout.addLayout(self.parentControlHorizontalLayout)
        self.parentControlLabel = QtWidgets.QLabel()
        self.parentControlLabel.setText('Parent Control:')
        self.parentControlHorizontalLayout.addWidget(self.parentControlLabel)
        
        #makes a text box to hold the name of the parent control 
        self.parentControlTextBox = QtWidgets.QLineEdit()
        self.parentControlTextBox.setReadOnly(True)
        self.parentControlTextBox.setMaximumSize(180, 20)
        self.parentControlTextBox.setMinimumSize(180, 20)
        self.parentControlHorizontalLayout.addWidget(self.parentControlTextBox)
        
        #makes a button to identify the selected control as the parent control 
        self.parentControlButton = QtWidgets.QPushButton()
        self.parentControlButton.setText('Add Selected Control')
        self.parentControlHorizontalLayout.addWidget(self.parentControlButton)
        self.spacerParent = QtWidgets.QSpacerItem(240, 10)
        self.parentControlHorizontalLayout.addItem(self.spacerParent)
        
        #makes a label for the child control
        self.childControlHorizontalLayout = QtWidgets.QHBoxLayout()
        self.verticalMidLayout.addLayout(self.childControlHorizontalLayout)
        self.childControlLabel = QtWidgets.QLabel()
        self.childControlLabel.setText('Child Control:')
        self.childControlHorizontalLayout.addWidget(self.childControlLabel)
        
        #makes a text box to hold the name of the child control
        self.childControlTextBox = QtWidgets.QLineEdit()
        self.childControlTextBox.setReadOnly(True)
        self.childControlTextBox.setMaximumSize(180, 20)
        self.childControlTextBox.setMinimumSize(180, 20)
        self.childControlHorizontalLayout.addWidget(self.childControlTextBox)
        
        #makes a button to identify the selected control as the child control 
        self.childControlButton = QtWidgets.QPushButton()
        self.childControlButton.setText('Add Selected Control')
        self.childControlHorizontalLayout.addWidget(self.childControlButton)
        self.spacerChild = QtWidgets.QSpacerItem(240, 10)
        self.childControlHorizontalLayout.addItem(self.spacerChild)
        
        #makes a button to parent the parent and child controls together 
        self.parentControlsButton = QtWidgets.QPushButton()
        self.parentControlsButton.setText('Parent Controls')
        self.parentControlsButton.setMinimumSize(560, 40)
        self.parentControlsButton.setMaximumSize(560, 40)
        self.verticalMidLayout.addWidget(self.parentControlsButton)

        self.setCentralWidget(self.window)
      
    #function for connecting UI signals to functions 
    def connectSignals(self):
        QtCore.QObject.connect(self.ctrlButton, QtCore.SIGNAL('clicked()'), self.makeCtrls)
        QtCore.QObject.connect(self.worldCtrlButton, QtCore.SIGNAL('clicked()'), self.makeWorldCtrl)
        QtCore.QObject.connect(self.worldParentButton, QtCore.SIGNAL('clicked()'), self.parentWorld)
        QtCore.QObject.connect(self.cogButton, QtCore.SIGNAL('clicked()'), self.makeCog)
        QtCore.QObject.connect(self.parentControlButton, QtCore.SIGNAL('clicked()'), self.getSelectedParentControl)
        QtCore.QObject.connect(self.childControlButton, QtCore.SIGNAL('clicked()'), self.getSelectedChildControl)
        QtCore.QObject.connect(self.parentControlsButton, QtCore.SIGNAL('clicked()'), self.parentCtrls)
        QtCore.QObject.connect(self.ctrlTypeButtonGroup, QtCore.SIGNAL('buttonClicked(int)'), self.enable)
        
    #makes a bold label for the UI   
    def makeTitleLabel(self, label, layout):
        self.Label = QtWidgets.QLabel()
        self.Label.setText('<b>' + label + '<\b>')
        layout.addWidget(self.Label)
    
    #makes a line for the UI    
    def makeLine(self, layout):
        self.line = QtWidgets.QFrame()
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        layout.addWidget(self.line)
    
    #this function is for adding items to the dropdown menus     
    def populateJointDropdowns(self):
        #finds all the joints in the scene
        self.intialJointList = self.findJoints()
        #adds found joints to the dropdown menus 
        for dropdown in range(len(self.dropdownList)):
            for joint in range(len(self.intialJointList)):
                self.dropdownList[dropdown].addItem(str(self.intialJointList[joint]))

    #this function finds all the joints in the scene 
    def findJoints(self):
        #gets all objects with type joint in the scene
        joints = pm.ls(et = 'joint')
        return joints

    #duplicates joints based off given joint list
    def duplicateJoints(self, jointList, prefix):
        dupJointList = []
        #duplicates all joints in joint list without their children and adds them to a list
        for joint in jointList:
            dupJoint = pm.duplicate(joint, name = prefix + str(joint), po = True)
            pm.parent(dupJoint[0], world = True)
            dupJointList.append(dupJoint)
        
        #parents the joints together     
        for i in range(len(dupJointList) -1):
            prnt = dupJointList[i +1]
            child = dupJointList[i]
            self.parentObject(prnt[0], child[0])
            
        #hides the created joints to clean up the viewport
        pm.hide(dupJointList[len(dupJointList) - 1])
        
        #returns the duplicated joints
        return dupJointList

    #makes Ik handle for given start and end joints
    def makeIk(self, ctrlType):
        if self.startJoint == self.endJoint:
            ikChainWarning = QtWidgets.QMessageBox()
            ikChainWarning.setWindowTitle('Warning')
            ikChainWarning.setText('Can\'t make an Ik chain one joint in length. Please select two different joints to continue.')
            ikChainWarning.exec_()
            #deletes the created control joints that were made by the make controls function
            ctrlJoint = self.findCtrlJoint(self.startJoint)
            pm.delete(ctrlJoint)
        else:
            #makes joints to be driven by ik controls directly 
            ikJoints = self.duplicateJoints(self.jointList, 'IK_')
            #for the joints in the list of ikJoints
            for j in range(len(ikJoints)):
                #if not being used for an IK/FK switch constrain control joints
                if self.switch == False:
                    ctrlJoint = self.findCtrlJoint(self.jointList[j])
                    self.parentConstrainObject(ikJoints[j], ctrlJoint)
       
            #makes the Ik handle
            handle = pm.ikHandle(sj = ikJoints[len(ikJoints) - 1][0], ee = ikJoints[0][0])
            #hides the handle to clean up the veiwport
            pm.hide(handle[0])
        
            #makes a control 
            ctrl = self.getSetPostion((10.0 * self.scaleFactor), 'IK_' + str(self.endJoint), self.endJoint, ctrlType)
            
            #hides attributes on the ik control that the user doesn't need
            attrList = ['scaleX', 'scaleY', 'scaleZ', 'visibility']
            for attr in attrList:
                pm.setAttr(str(ctrl[1][0]) + '.' + attr,  k = False, cb = False)
            
            #parents the IK handle under the ctrl 
            self.parentObject(ctrl[1][0], handle[0])
            
            #makes a control for the pole vector 
            poleCtrl = self.getSetPostion((5.0 * self.scaleFactor), 'IK' + str(self.middleJoint) + '_Pole_Vector', self.middleJoint, ctrlType)
            
            #hides attributes the pole vector control doesn't need 
            for attr in attrList:
                pm.setAttr(str(poleCtrl[1][0]) + '.' + attr,  k = False, cb = False)
            
            #finds offset group for the pole vector control
            children = pm.listRelatives(poleCtrl[0], ad = True)
            offset = children[len(children)-1]
            
            #gets the world space postion of the joint to use for placing the pole vector 
            jointTrans = pm.xform(self.middleJoint, query = True, ws = True, t = True)
            #determines the x, y and z values to move the pole vector control based off user selection 
            #if the user selected front 
            if self.poleVectorPostion == -2:
                x = jointTrans[0]
                y = jointTrans[1]
                z = (100 * self.scaleFactor)
            #if the user selected back
            elif self.poleVectorPostion == -3:
                x = jointTrans[0]
                y = jointTrans[1]
                z = (-100 * self.scaleFactor)
            #if the user selcted right 
            elif self.poleVectorPostion == -4:
                x = (-100 * self.scaleFactor)
                y = jointTrans[1]
                z = jointTrans[2]
            #if the user selcted left 
            elif self.poleVectorPostion == -5:
               x = (100 * self.scaleFactor)
               y = jointTrans[1]
               z = jointTrans[2]
           #if the user didn't make a selection gives a warning 
            else:
               poleVectorPostionWarning = QtWidgets.QMessageBox()
               poleVectorPostionWarning.setWindowTitle('Warning')
               poleVectorPostionWarning.setText('No pole vector postion selected. Please select a pole vector postion to continue.')
               poleVectorPostionWarning.exec_()
              
               #removes non functioning partial rig
               pm.delete(ikJoints)
               pm.delete(poleCtrl)
               pm.delete(ctrl)
               ctrlJoint = self.findCtrlJoint(self.startJoint)
               pm.delete(ctrlJoint)
               return
            
            #moves the pole vector
            pm.xform(offset, ws = True, t = (x,y,z))
            #constrains the ik handle to the pole vector 
            pm.poleVectorConstraint(poleCtrl[1][0], handle[0])
                  
            #makes a control for the top of the ik chain and constrains the ik chain to it 
            topCtrl = self.getSetPostion((10.0 * self.scaleFactor), 'Ik_' + str(self.startJoint), self.startJoint, ctrlType)
            self.parentConstrainObject(topCtrl[1][0], ikJoints[len(ikJoints) - 1])
            
            #locks and hides unnecessary attributes from the control
            for attr in attrList:
                pm.setAttr(str(topCtrl[1][0]) + '.' + attr, k = False, cb = False)
               
            #tries to find a child joint to make a secondary ik handle to enable rotation of the end of the ik chain
            try:
                #finds the children of the end joint 
                childJoint = pm.listRelatives(self.endJoint, c = True, type = 'joint')[0]
                childJointList = [childJoint]
                
                #makes an ik joint and parents it to the rest of the ik chain 
                ikChildJoint = self.duplicateJoints(childJointList, 'IK_')
                self.parentObject(ikJoints[0][0], ikChildJoint[0])
        
                #makes an ik handle and parents it the other handle to enable rotation at the end of the ik chain 
                ikChildHandle = pm.ikHandle(sj = ikJoints[0][0], ee = ikChildJoint[0][0])
                self.parentObject(handle[0], ikChildHandle[0])
                
                #hides the ik handles 
                pm.hide(ikChildHandle[0])
            
            #if there are no child joints lets the user know that rotation won't work but leaves the control    
            except:
                noChildWarning = QtWidgets.QMessageBox()
                noChildWarning.setWindowTitle('Warning')
                noChildWarning.setText('No child joints after the end of the IK chain. The control on the end of the chain will not be able to rotate.')
                noChildWarning.exec_()

            #returns the list of ik joints and all the controls for use in ik/fk switching function
            return ikJoints, ctrl, poleCtrl, topCtrl
        
    #parents objects given a parent and a child object        
    def parentObject(self, parentObject, childObject):
        pm.parent(childObject, parentObject)
        
    #parent constrains 2 objects
    def parentConstrainObject(self, parent, child):
        pm.parentConstraint(parent, child)
    
    #this function makes controls using nurbs circles     
    def makeCtrl(self, radius = 50, name = 'circle', ctrlType = ''):
        #makes a nurbs circle
        ctrl = pm.circle(r = radius,n = name + '_ctrl', nr = (1.0, 0.0, 0.0))
        
        #gets the shape associated with the control 
        shape = pm.listRelatives(ctrl, ad = True, s = True)
        #allows color to be changed 
        pm.setAttr(shape[0] + '.overrideEnabled', True)
        #if it's a middle control make it yellow
        if ctrlType == -2:
            pm.setAttr(shape[0] + '.overrideColor', 17)
        #if it's a right control make it red
        elif ctrlType == -3:
            pm.setAttr(shape[0]+'.overrideColor', 13)
        #if it's a left control make it blue
        elif ctrlType == -4:
            pm.setAttr(shape[0] + '.overrideColor', 6)
        #if it's an extra control or the user didn't specify make it green 
        else:
            pm.setAttr(shape[0] + '.overrideColor', 14)
            
        #make offset and parent groups 
        offset = pm.group(ctrl, n = 'offset_' + name)
        prnt = pm.group(offset, n = 'prnt_' + name)
        
        #returns parent group and the circle object
        return prnt, ctrl
        
    #places controls around joint   
    def getSetPostion(self, radius, name, joint, ctrlType):
        ctrl = self.makeCtrl(radius, name, ctrlType)
        
        #gets joint translation 
        t = pm.xform(joint, translation = True, query = True, ws = True)
        #gets joint rotation
        r = pm.xform(joint, rotation = True, query = True, ws = True)
       
        #places the control 
        pm.move(ctrl[0], t)
        pm.rotate(ctrl[0], (r[0], r[1], r[2]))
        return ctrl

    #this function sets up an fk control given a skinning joint 
    def makeFKCtrl(self, skJoint, fkJoint, name, ctrlType):
        joint = self.findCtrlJoint(skJoint)
        print 'control joint fk', joint
        
        #if this chain is not for an IK/FK switch parent constrain control joint to the fk joint 
        if self.switch == False:
            #constrains the control joint to the fk joint 
            self.parentConstrainObject(fkJoint, joint)
        
        #makes a control and places it on the fk joint
        ctrl = self.getSetPostion((10.0 * self.scaleFactor), name, fkJoint, ctrlType)
        #constrains the fk joint to the fk control 
        self.parentConstrainObject(ctrl[1], fkJoint)
        
        #hides unnecessary attributes on the control 
        attrList = ['translateX', 'translateY', 'translateZ', 'scaleX', 'scaleY', 'scaleZ', 'visibility']
        for attr in attrList:
            pm.setAttr(str(ctrl[1][0]) + '.' + attr, k = False, cb = False)
        
        return ctrl
    
    #makes a chain of fk controls for all the specified joint and it's children     
    def makeFKChain(self, ctrlType):
        #makes joints to be driven by fk controls directly 
        fkJoints = self.duplicateJoints(self.jointList, 'FK_')

        #ctrlList will contain ctrl and prnt groups 
        #starting with bottom of the chain 
        self.ctrlList = []
        #makes controls and adds there prnt groups and ctrls to a list
        for joint in range(len(fkJoints)):
            childName = str(fkJoints[joint][0])
            childCtrl = self.makeFKCtrl(self.jointList[joint], fkJoints[joint], childName, ctrlType)
            self.ctrlList.append(childCtrl)
        
        #parents the fk controls together 
        for i in range(len(self.ctrlList)-1):
            prnt = self.ctrlList[i +1]
            child = self.ctrlList[i]
            self.parentObject(prnt[1][0], child[0])
            
        return fkJoints

    #makes a control to hold an IK, FK switch 
    def makeIkFkSwitchCtrl(self, name, ctrlType):
        ctrl = self.makeCtrl((5.0 * self.scaleFactor), name, ctrlType)
        #gets all the keyable attributes(ones found in channel box)
        channelAttr =  pm.listAttr(ctrl[1][0], k = True)
        #this locks and hides the attributes 
        for attr in channelAttr:
            pm.setAttr(ctrl[1][0] + '.' + attr, l = True, k = False, cb = False)
        #adds attribute for IK/FK switch      
        pm.addAttr(ctrl[1][0], ln = 'IK_FK_Switch', at = 'float', max = 1.0, min = 0.0, k = True)
        return ctrl
        
    #makes an Ik/Fk switch     
    def ikFkSwitch(self, fkJoint, IkJoint, skJoint):
        #makes a control for the ik/fk switch attribute
        ctrl = self.makeIkFkSwitchCtrl('Switch', 'Extra')

        #gets the Ik/Fk switch attribute off the Ik/Fk control
        switchAttr =  pm.listAttr(ctrl[1][0], c = True, k = True)[0]

        #constrains the rest of the joints and keeps track of them in a list
        constraintList = []
        for j in range(len(fkJoint)):
            ctrlJoint = self.findCtrlJoint(self.jointList[j])
            childC = pm.parentConstraint(fkJoint[j], IkJoint[0][j], ctrlJoint)
            constraintList.append(childC)

        #make a reverse node
        reverseNode = pm.shadingNode('reverse', asUtility = True)
        #connect the switch attribute to the input of the reverse node 
        pm.connectAttr(ctrl[1][0] + '.' + switchAttr, reverseNode + '.input.inputX')
       
        #connect the constraint weights to the fk/ik switch 
        #also connects control visibility to the switch 
        for constraint in range(len(constraintList)):
            attributes = pm.listAttr(constraintList[constraint], c = True, k = True)
            pm.connectAttr(ctrl[1][0] + '.' + switchAttr, constraintList[constraint] + '.' + attributes[len(attributes) -1])
            pm.connectAttr(reverseNode + '.output.outputX', constraintList[constraint] + '.' + attributes[len(attributes) -2]) 
            pm.connectAttr(reverseNode + '.output.outputX', self.ctrlList[constraint][1][0] + '.visibility') 
            pm.connectAttr(ctrl[1][0] + '.' + switchAttr, IkJoint[constraint + 1][0] + '.visibility')
    
        #positions the Ik/Fk switch opposite to the position of the pole vector
        ctrlJoint = self.findCtrlJoint(skJoint)
        self.parentConstrainObject(ctrlJoint, ctrl[0])
        child = pm.listRelatives(ctrl[0], c = True, type = 'transform')
        offset = child[0]
        ctrlJointTrans = pm.xform(ctrlJoint, query = True, ws = True, t = True)
        #if the user picked front
        if self.poleVectorPostion == -2:
            x = ctrlJointTrans[0]
            y = ctrlJointTrans[1]
            z = (-20 * self.scaleFactor)
        #if the user picked back 
        elif self.poleVectorPostion == -3:
            x = ctrlJointTrans[0]
            y = ctrlJointTrans[1]
            z = (20 * self.scaleFactor)
        #if the user picked right
        elif self.poleVectorPostion == -4:
            x = (20 * self.scaleFactor)
            y = ctrlJointTrans[1]
            z = ctrlJointTrans[2]
        #if the user picked left
        else:
            x = (-20 * self.scaleFactor)
            y = ctrlJointTrans[1]
            z = ctrlJointTrans[2]
        #places the switch in the world
        pm.xform(offset, ws = True, t = (x, y, z))

    #duplicates joints to make a ctrl skeleton     
    def makeCtrlSkeleton(self):
        #makes joints to be driven by fk controls directly 
        self.ctrlJoints = self.duplicateJoints(self.jointList, 'ctrl_')
        
        for joint in range(len(self.jointList)):
            self.parentConstrainObject(self.ctrlJoints[joint], self.jointList[joint])
             
        return self.ctrlJoints

    #finds ctrl joint to match the given skinning joint      
    def findCtrlJoint(self, skJoint):
        skName = str(skJoint)
        #iterates through the list looking for the corresponding control joint 
        for j in range(len(self.ctrlJoints)):
            #if it finds a match it returns the joint
            if str(self.ctrlJoints[j][0]).endswith(skName) == True:
                return self.ctrlJoints[j]

    #function for making controls once the button is pressed            
    def makeCtrls(self):
        #get control type state 
        ControlType = self.ctrlTypeButtonGroup.checkedId()
        #if no type was specified gives the user a warning
        if ControlType == -1: 
            controlTypeWarning = QtWidgets.QMessageBox()
            controlTypeWarning.setWindowTitle('Warning')
            controlTypeWarning.setText('No control type selected. Please select control type to continue')
            controlTypeWarning.exec_()
        else:    
            #get relevant joints 
            self.startJoint = self.getJoint(self.Dropdown1)
            self.endJoint = self.getJoint(self.Dropdown2)
            self.middleJoint = self.getJoint(self.midJointDropdown)
            ctrlColor = self.ctrlLocationButtonGroup.checkedId()
            #checks that the scale factor is valid
            scaleFactorTest = self.scaleFactorTextBox.text()
            #if it isn't gives the user a warning
            if scaleFactorTest.count('.') > 1 or scaleFactorTest == '' or  float(scaleFactorTest) == 0:
                scaleFactorWarning = QtWidgets.QMessageBox()
                scaleFactorWarning.setWindowTitle('Warning')
                scaleFactorWarning.setText('Scale entered is invalid. Please enter vaild scale to continue.')
                scaleFactorWarning.exec_()
            #if it is makes the controls     
            else:
                self.scaleFactor = float(scaleFactorTest)
                #make a list to hold joints that will have controls 
                self.jointList = []
                joint = self.endJoint
        
                #this gives a list of joints from start to end joint 
                #gives a complete list of skJoints 
                while str(self.startJoint) != str(joint):
                    self.jointList.append(joint)
                    jointParent = pm.listRelatives(joint, p = True)[0]
                    joint = jointParent 
                    
                self.jointList.append(self.startJoint)
                #finds all the joints currently in the scene
                jointsInScene = self.findJoints()
                
                #Checks to make sure that the joints don't already have controls before rigging them 
                for joint in self.jointList:
                    ctrlJointName = 'ctrl_' + str(joint)
                    for j in jointsInScene:
                        #if they do have controls gives the user a warning 
                        if str(j) == ctrlJointName:
                            controlsExistWarning = QtWidgets.QMessageBox()
                            controlsExistWarning.setWindowTitle('Warning')
                            controlsExistWarning.setText('Joints in range of start and end joint already have controls. Pick joints without controls to continue.')
                            controlsExistWarning.exec_()
                            return
                            
                self.poleVectorPostion = self.postionButtonGroup.checkedId()
        
                #duplicate joints
                #assume not making an FK/IK switch 
                self.switch = False
        
                self.ctrlRoot = self.makeCtrlSkeleton() 
                
                #if control type = -3  
                #make ik controls
                if ControlType == -3:
                    ikJoint = self.makeIk(ctrlColor)    
        
                #if control type is -4
                #make an Ik/Fk switch
                elif ControlType == -4:
                    self.switch = True
                    fkJoint = self.makeFKChain(ctrlColor)
                    ikJoint = self.makeIk(ctrlColor) 
                    ctrlJoint = self.findCtrlJoint(self.startJoint)
                    self.ikFkSwitch(fkJoint, ikJoint, self.endJoint)
                    
                #make fk chain 
                else: 
                    fkJoint = self.makeFKChain(ctrlColor)
                
    #makes the world control for the rig             
    def makeWorldCtrl(self):
        #looks to see if there is a world control already in the scene
        transforms = pm.ls(type = 'transform')
        worldList = []
        for trans in range(len(transforms)):
            if transforms[trans].endswith('World') == True:
                worldList.append(transforms[trans])
        #if there is already a world control in the scene give the user a warning
        if worldList:
            worldControlWarning = QtWidgets.QMessageBox()
            worldControlWarning.setWindowTitle('Warning')
            worldControlWarning.setText('There is already a world control made. There can only be one world control per rig.')
            worldControlWarning.exec_()
        #if not continues to the scale factor warning test
        else:
            name = 'World'
            #checks to see that the user input scale is valid 
            scaleFactorTest = self.worldScaleTextBox.text() 
            #if it isn't gives the user a warning        
            if scaleFactorTest.count('.') > 1 or scaleFactorTest == '' or  float(scaleFactorTest) == 0:
                scaleFactorWarning = QtWidgets.QMessageBox()
                scaleFactorWarning.setWindowTitle('Warning')
                scaleFactorWarning.setText('Scale entered is invalid. Please enter vaild scale to continue.')
                scaleFactorWarning.exec_()
            #if the scale factor is valid makes a world control 
            else:
                scaleFactor = float(scaleFactorTest)        
                self.worldCtrl = pm.circle(r = (100 * scaleFactor), name = name, nr = (0.0, 1.0, 0.0))
                
                #hides attributes on the control that are unnecessary 
                attrList = ['scaleX', 'scaleY', 'scaleZ', 'visibility']
                for attr in attrList:
                    pm.setAttr(str(self.worldCtrl[0]) + '.' + attr, l = True, k = False, cb = False)
                    
                #gets the shape associated with the control 
                shape = pm.listRelatives(self.worldCtrl, ad = True, s = True)
                #allows color to be changed 
                pm.setAttr(shape[0] + '.overrideEnabled', True)
                pm.setAttr(shape[0] + '.overrideColor', 17)
                    
                #make offset and parent groups 
                offset = pm.group(self.worldCtrl, n = 'offset_' + name)
                prnt = pm.group(offset, n = 'prnt_' + name)

    #function for making the world control     
    def parentWorld(self):
        #tries to parent all controls and control joints to the world control 
        try:
            #gets list of top level items in the scene
            topLevelList =  pm.ls(assemblies = True)  
            list = []
            #filters through list for all controls and control joints made except for the world control
            for i in range(len(topLevelList)):
                if (str(topLevelList[i])[:2] == ('IK')) or (str(topLevelList[i])[:2] == ('FK')) or ((str(topLevelList[i])[:4] == 'prnt') and str(topLevelList[i]).endswith('World') == False)  or (str(topLevelList[i])[:4] == 'ctrl'):
                    list.append(topLevelList[i])
    
            #parents items in the list to the world control 
            for j in range(len(list)):
                self.parentObject(self.worldCtrl[0], list[j])
        #if it fails tells the user that there isn't a world control         
        except:
            parentWorldWarning = QtWidgets.QMessageBox()
            parentWorldWarning.setWindowTitle('Warning')
            parentWorldWarning.setText('No world control in the scene. Please make a world control to continue.')
            parentWorldWarning.exec_()

    #makes a cog control for the rig         
    def makeCog(self):
        #gets the user identified cog joint
        cogJoint = self.getJoint(self.cogDropdown)
        #gets scale factor for cog control
        scaleFactorTest = self.cogScaleTextBox.text()
        #checks the scale factor is valid
        if scaleFactorTest.count('.') > 1 or scaleFactorTest == '' or  float(scaleFactorTest) == 0:
            scaleFactorWarning = QtWidgets.QMessageBox()
            scaleFactorWarning.setWindowTitle('Warning')
            scaleFactorWarning.setText('Scale entered is invalid. Please enter vaild scale to continue.')
            scaleFactorWarning.exec_()
        #if it is makes a cog control 
        else:    
            scaleFactor = float(scaleFactorTest)     
            #makes the cog control
            ctrl = self.getSetPostion((25.0 * scaleFactor), 'COG', cogJoint, -2)
            #locks and hides unnecessary attributes on the control 
            attrList = ['scaleX', 'scaleY', 'scaleZ', 'visibility']
            for attr in attrList:
                pm.setAttr(str(ctrl[1][0]) + '.' + attr, l = True, k = False, cb = False)

    #gets the selected control and stores it as the parent control   
    def getSelectedParentControl(self):
        self.parentSelected = pm.ls(selection = True)
        self.parentControlTextBox.setText(str(self.parentSelected[0]))
    
    #gets the selected control and stores it as the child control
    def getSelectedChildControl(self):
        self.childSelected = pm.ls(selection = True)
        self.childControlTextBox.setText(str(self.childSelected[0]))
 
    #parents the parent group of the child control to the parent control    
    def parentCtrls(self):
        #tries to parent the controls
        try:
            #because of group structure controls are parent with the prnt group of the child control under the control of the prnt
            #finds the prnt group of the child control 
            childOffset = pm.listRelatives(self.childSelected[0], ap = True)
            childPrntGroup = pm.listRelatives(childOffset[0], ap = True)
            #parents the prnt group for the child control under the parent control 
            self.parentObject(self.parentSelected[0], childPrntGroup[0])
        #if it fails gives the user a warning that the selected controls aren't valid
        except:
            parentControlsWarning = QtWidgets.QMessageBox()
            parentControlsWarning.setWindowTitle('Warning')
            parentControlsWarning.setText('Invalid control selection.')
            parentControlsWarning.exec_()

    #disables the parts of the UI used for making pole vectors if not making an ik chain 
    def enable(self):
        activeControlType = self.ctrlTypeButtonGroup.checkedId()
        #if making an ik chain enable part of the UI for making pole vectors  
        if activeControlType == -3 or activeControlType == -4:
            self.midJointLabel.setDisabled(False)
            self.midJointDropdown.setDisabled(False)
            self.polevectorLabel.setDisabled(False)
            self.frontButton.setDisabled(False)
            self.frontLabel.setDisabled(False)
            self.backButton.setDisabled(False)
            self.backLabel.setDisabled(False)
            self.rightButton2.setDisabled(False)
            self.rightLabel2.setDisabled(False)
            self.leftButton2.setDisabled(False)
            self.leftLabel2.setDisabled(False)
            
        #if making only fk controls or the user hasn't make a choice disables the UI for making pole vectors   
        else:
            self.midJointLabel.setDisabled(True)
            self.midJointDropdown.setDisabled(True)
            self.polevectorLabel.setDisabled(True)
            self.frontButton.setDisabled(True)
            self.frontLabel.setDisabled(True)
            self.backButton.setDisabled(True)
            self.backLabel.setDisabled(True)
            self.rightButton2.setDisabled(True)
            self.rightLabel2.setDisabled(True)
            self.leftButton2.setDisabled(True)
            self.leftLabel2.setDisabled(True)
        
    #gets joint associated with name in a dropdown menu     
    def getJoint(self, dropDown):
        jointName = dropDown.currentText()
        skJoint = 'None'
        for joint in range(len(self.intialJointList)):
            #compares the joint name in the dropdown to the skinning joints name
            if str(self.intialJointList[joint]).endswith(jointName) == True:
                #if it matches stores the joint in the varible sk joint 
                skJoint = self.intialJointList[joint]
        return skJoint 
        
#---------------
#call
#---------------
ctrlRigUI() 