from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
from nodemodel import NodeModel

class NodeTable(QTableWidget):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.setColumnCount(6)
        self.nodeModel = NodeModel("nodes\nodes.json")
