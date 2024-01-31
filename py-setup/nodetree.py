from PySide6.QtWidgets import QTreeView ,QTreeWidget, QTreeWidgetItem, QMenu, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction,QIcon
from nodemodel import NodeModel
from nodeedit import NodeEditDlg
#from mainwindow import MainWindow
from prebootout import PreBootOut
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
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

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
        itemName = item.text(0)
        if itemName != "Nodes":
            dlg =  NodeEditDlg(self,self.nodeModel, "Edit Node")
            model = self.nodeModel
            node = model.getNodeByName(itemName)
            if node:
                    dlg.fillNode(node)
            dlg.exec()
#        for node in self.nodeArr:
#            if node['name'] == item.text(0):
#                dlg.fillNode(node)
#        dlg.exec()
        self.reloadTree()

    def _show_context_menu(self, position):
        print(position)
        node = self.selectedItems()
        nodeName = node[0].data(0,0)
        print("Select " + nodeName)
        if nodeName != "Nodes":
            ctx_act_edit= QAction("Edit")
            ctx_act_edit.triggered.connect(self.editNode)
            ctx_act_dub = QAction("Dublicate")
            ctx_act_dub.triggered.connect(self.dublicateNode)
            ctx_act_del = QAction("Delete")
            ctx_act_del.triggered.connect(self.deleteNode)

            ctx_act_preb = QAction("Preboot output")
            ctx_act_preb.triggered.connect(self.preeBootNode)

            menu = QMenu(self)
            menu.addAction(ctx_act_edit)
            menu.addAction(ctx_act_dub)
            menu.addAction(ctx_act_del)
            menu.addSeparator()
            menu.addAction(ctx_act_preb)
            menu.exec_(self.mapToGlobal(position))

    def editNode(self):
        node = self.selectedItems()
        item = node[0]
        self.onClickItem(item)

    def dublicateNode(self):
        TrNodes = self.selectedItems()
        item = TrNodes[0]
        itemName = item.text(0)
        model = self.nodeModel
        node = model.getNodeByName(itemName).copy()
        node['name'] = node['name'] + '_1'
        model.addNode(node)
        self.reloadTree()

    def deleteNode(self):
        TrNodes = self.selectedItems()
        item = TrNodes[0]
        itemName = item.text(0)
        model = self.nodeModel
        node = model.getNodeByName(itemName)
        button = QMessageBox.question(self, "Delete Node", "Want to delete node " + itemName)
        if button == QMessageBox.Yes:
            model.removeNode(node)
        self.reloadTree()

    def preeBootNode(self):
        TrNodes = self.selectedItems()
        item = TrNodes[0]
        itemName = item.text(0)
        model = self.nodeModel
        node = model.getNodeByName(itemName)
        dlg = PreBootOut(self,model)
        dlg.selectNode(node)
        dlg.exec()
