'''
This is a script for making a UI that is more complex. 
'''
from pyfbsdk import *
from PySide import QtGui, QtCore 

class complexUI(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(complexUI, self).__init__(parent)
        self.makeUI()
        self.show()
        self.connectSignals()
    
    def connectSignals(self):
        QtCore.QObject.connect(self.button, QtCore.SIGNAL('clicked()'), self.buttonPressed)
    
    def makeUI(self):
        #makes the main window 
        self.window = QtGui.QWidget()
        self.setWindowTitle('Test')
        self.resize(520, 500)
        self.setMinimumSize(520, 500)
        self.setMaximumSize(520, 500)
        self.verticalWindowLayout = QtGui.QVBoxLayout(self.window)
       
        
        #makes a frame 
        self.frame = QtGui.QFrame(self.window)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.verticalFrameLayout = QtGui.QVBoxLayout(self.frame)
        
        self.button = QtGui.QPushButton()
        self.button.setMinimumSize(460, 40)
        
        self.scrollArea = QtGui.QScrollArea()
        self.scrollWidget = QtGui.QWidget()
        self.scrollWidget.setMinimumSize(450,0)
        self.scrollLayout = QtGui.QVBoxLayout(self.scrollWidget)
        self.scrollArea.setWidget(self.scrollWidget)
        self.scrollArea.setAlignment(QtCore.Qt.AlignTop)
        

        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.verticalFrameLayout.addWidget(self.scrollArea)
        
        self.verticalFrameLayout.addWidget(self.button)
        
        self.verticalWindowLayout.addWidget(self.frame)
        self.setCentralWidget(self.window)
        #list to hold all the created widgets that are added to the scroll area
        self.widgetList = []
        
    def buttonPressed(self):
        self.expand = True
        self.scrollResize()
        frame = QtGui.QFrame()
        frame.setFrameShape(QtGui.QFrame.StyledPanel)
        frame.setAutoFillBackground(True)
        frame.setBackgroundRole(QtGui.QPalette.Midlight)
        frame.setMaximumSize(440, 80)
        horizontalLayout = QtGui.QHBoxLayout(frame)
        label = QtGui.QLabel()
        label.setText('Test:')
        horizontalLayout.addWidget(label)
        button = QtGui.QPushButton()
        button.setText('Delete')
        button.setMinimumSize(300, 40)
        QtCore.QObject.connect(button, QtCore.SIGNAL('clicked()'), self.delete)
        horizontalLayout.addWidget(button)
        self.scrollLayout.addWidget(frame)
        self.widgetList.append(frame)
        
       
    #it's going to remove the widget     
    def delete(self):
        self.expand = False
        buttonPressed = self.sender()
        parentWidget = buttonPressed.parentWidget()
        parentWidget.deleteLater()
        self.scrollResize()
        
        
    #expands the scroll space to match the new widgets     
    def scrollResize(self):
        widgetSize = self.scrollWidget.size()
        currentHeight = widgetSize.height()
        width = widgetSize.width()
        if self.expand == True:
            #adds a little more than the height of the widget to the space
            height = currentHeight + 90
        else:
            height = currentHeight - 90
        self.scrollWidget.resize(width, height)
        

test = complexUI()