import os.path
import json
from config import *

class NodeModel:
    def __init__(self, filename):
        self.filename = filename
        self.model = []
        self.isModify = False

    def Load(self):
        if os.path.isfile(self.filename):
             fname = self.filename
        else:
             fname = NODES_SAMPLE

        with open(fname) as file_object:
                # store file data in object
                self.model = json.load(file_object)        
    
    def Save(self):
        try:
            with open(self.filename, "w") as file_write:
            # write json data into file
                json.dump(self.model, file_write)
                self.isModify = False
        except:
            print("Something went wrong")
   
    def getModel(self):
         return self.model

    def setModel(self, model):
         self.model = model
    
    def getNodeArry(self):
         return self.model['nodes']
    
    def addNode(self,node):
         self.isModify = True
         self.model['nodes'].append(node)

    def removeNode(self,node):
         self.isModify = True
         self.model['nodes'].remove(node)

    def getSettings(self):
         return self.model['settings']