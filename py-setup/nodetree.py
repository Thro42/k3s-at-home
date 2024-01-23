from PySide6.QtWidgets import QTreeView ,QTreeWidget, QTreeWidgetItem
from nodemodel import NodeModel
from nodeedit import NodeEditDlg
#from mainwindow import MainWindow
from config import *


class NodeTree (QTreeWidget) :
    HEADER = ('Name', 'IP', 'network', 'os', 'typ', 'rolle')
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.nodeModel = NodeModel(NODES_BASE)
        self.setColumnCount(len(self.HEADER))
        #self.setHeaderLabels(('Name', 'IP', 'network', 'os', 'typ', 'rolle'))
        self.setHeaderLabels(self.HEADER)
        # self.resize(window.)
        self.itemDoubleClicked.connect(self.onClickItem)

    def loadTree(self):
        self.nodeModel.Load()
        rootNodse = QTreeWidgetItem(('Nodes',))
        self.nodeArr = self.nodeModel.getNodeArry()
        #print( self.nodeArr)
        for node in self.nodeArr:
            #print("node:", node)
            tNNode = QTreeWidgetItem((node['name'],node['ip'],node['network'],node['os'],node['typ'],node['rolle']))
            rootNodse.addChild(tNNode)
        self.addTopLevelItem(rootNodse)
        self.expandAll()

    def getTreeModel(self):
        return self.nodeModel
    
    def reloadTree(self):
        self.clear()
        rootNodse = QTreeWidgetItem(('Nodes',))
        self.nodeArr = self.nodeModel.getNodeArry()
        #print( self.nodeArr)
        for node in self.nodeArr:
            #print("node:", node)
            tNNode = QTreeWidgetItem((node['name'],node['ip'],node['network'],node['os'],node['typ'],node['rolle']))
            rootNodse.addChild(tNNode)
        self.addTopLevelItem(rootNodse)
        self.expandAll()

    def onClickItem(self,item):
        model = self.nodeModel
        dlg =  NodeEditDlg(self,self.nodeModel, "Edit Node")
        for node in self.nodeArr:
            if node['name'] == item.text(0):
                dlg.fillNode(node)
        dlg.exec()
        self.reloadTree()
