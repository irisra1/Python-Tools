"""
#############################################################################
filename    exportAnim.py
author      Iris Rahmel 
email    irisra@live.com

date modified    April 2, 2018
Brief Description:
    This is a script that does the preprocess for animations for game and 
    then exports it. 
#############################################################################
"""
import pymel.core as pm 

class ExportUI(object):
    def __init__(self):
        #makes the UI for the script in the intializer 
        myWindow = pm.window(title = 'Bake Keys')
        col = pm.columnLayout(adjustableColumn = True)
        self.save = pm.textFieldGrp(label = 'Save File As:', text = 'keys_baked')
      
        self.root = pm.textFieldGrp(label = 'Root Joint Name:', text = 'j_root')
        
       
        self.world = pm.textFieldGrp(label = 'World Group Name:', text = 'prnt_world')

        self.start =  pm.intFieldGrp(label = 'Start Frame:')
        self.end =  pm.intFieldGrp(label = 'End Frame:')
      
        button = pm.button(label = 'bake keys', command = self.bakeKeys)

        pm.showWindow(myWindow)
     
    #this function bakes keys onto the main skeleton and deletes the control rig 
    def bakeKeys(self, *args):
        #import the referenced rig and model 
        self.importReferences()
        
        self.bakeAnim()
        
        #deletes all constraints in the scene
        pm.delete(all = True, cn = True)
        #deletes the control rig
        pm.delete(self.world.getText())
        #save a new file 
        pm.saveAs(self.save.getText(), save = True, force = True, type = 'mayaAscii')
    
    #function imports referenced files 
    def importReferences(self):
       #loops twice because there were two refernce layers in our scenes
       for i in range(2):
            for ref in pm.listReferences():
                 ref.importContents()
                 
    #bakes down keys onto skinning skeleton         
    def bakeAnim(self,*args): 
        pm.bakeResults(self.root.getText(),sm = True, hi= 'below', t=(self.start.getValue()[0],self.end.getValue()[0]))
    
       
UI = ExportUI()