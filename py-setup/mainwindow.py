from PySide6.QtCore import QSize
from PySide6.QtGui import QAction,QIcon
from PySide6.QtWidgets import QMainWindow,QToolBar,QPushButton,QStatusBar,QMessageBox
from nodetree import NodeTree
from nodeedit import NodeEditDlg
from prebootout import PreBootOut
from settings import SettingDlg
from inventory import Inventory

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app #declare an app member
        self.setWindowTitle("k3 Node Setup")
        self.setWindowIcon(QIcon('images\pi_setup.png'))
        self.resize(800,600)
        #Menubar and menus
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")

        save_action = file_menu.addAction("Preboot output")
        save_action.triggered.connect(self.preboot_out)

        save_action = file_menu.addAction("Settings")
        save_action.triggered.connect(self.edit_setting)

        save_action = file_menu.addAction("Generate Inventory")
        save_action.triggered.connect(self.save_inventory)

        file_menu.addSeparator()
        save_action = file_menu.addAction("Save")
        save_action.triggered.connect(self.save_date)
        file_menu.addSeparator()

        quit_action = file_menu.addAction("Quit")
        quit_action.triggered.connect(self.quit_app)
        # Node menu
        edit_menu =menu_bar.addMenu("Node")
        add_action = edit_menu.addAction("Add")
        add_action.triggered.connect(self.add_node)

        #Working with toolbars
        toolbar = QToolBar("toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        #Add the quit action to the toolbar
        toolbar.addAction(quit_action)
        # Working with status bars
        self.setStatusBar(QStatusBar(self))

        self.nodeTree = NodeTree(self)
        self.nodeTree.loadTree()
        self.setCentralWidget(self.nodeTree)
        
    def quit_app(self):
        self.app.quit()

    def add_node(self):
        model = self.nodeTree.getTreeModel()
        dlg =  NodeEditDlg(self, model, "Add Node")
        dlg.exec()
        self.nodeTree.reloadTree()

    def save_date(self):
        model = self.nodeTree.getTreeModel()
        model.Save()

    def preboot_out(self):
        model = self.nodeTree.getTreeModel()
        dlg = PreBootOut(self,model)
        dlg.exec()

    def edit_setting(self):
        model = self.nodeTree.getTreeModel()
        dlg = SettingDlg(self, model)
        dlg.exec()

    def save_inventory(self):
        model = self.nodeTree.getTreeModel()
        nodeArr = model.getNodeArry()
        inventory = Inventory()
        inventory.generate(nodeArr)
        QMessageBox.information(self, 'Save Inventory', 'Inventory generated')
