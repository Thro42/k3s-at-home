from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QComboBox, 
    QDialogButtonBox, QFormLayout, QLabel, QLineEdit,
    QSizePolicy, QWidget)
from PySide6.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton

class NodeEditDlg(QDialog):
    def __init__(self, parent, model, title):
        super().__init__(parent)
        self.title = title
        self.model = model
        self.setWindowIcon(QIcon('images\pi_setup.png'))
        self.resize(387, 196)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(290, 20, 81, 151))
        self.buttonBox.setOrientation(Qt.Vertical)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.formLayoutWidget = QWidget(self)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(9, 9, 271, 176))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)

        self.nameLbl = QLabel(self.formLayoutWidget)
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.nameLbl)
        self.nameLbl.setText("Name")
        self.nameEdit = QLineEdit(self.formLayoutWidget)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.nameEdit)

        self.label_2 = QLabel(self.formLayoutWidget)
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)
        self.label_2.setText("IP Addr.")
        self.ipEdit = QLineEdit(self.formLayoutWidget)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.ipEdit)

        self.label_3 = QLabel(self.formLayoutWidget)
        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)
        self.label_3.setText("Network")

        self.networkCB = QComboBox(self.formLayoutWidget)
        self.networkCB.addItem("eth","eth")
        self.networkCB.addItem("wifi","wifi")
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.networkCB)

        self.label_4 = QLabel(self.formLayoutWidget)
        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_4)

        self.osCB = QComboBox(self.formLayoutWidget)
        self.osCB.addItem("ubuntu","ubuntu")
        self.osCB.addItem("buster","buster")
        self.osCB.addItem("bookworm","bookworm")
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.osCB)

        self.label_5 = QLabel(self.formLayoutWidget)
        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_5)

        self.typeCB = QComboBox(self.formLayoutWidget)
        self.typeCB.addItem("rp3","rp3")
        self.typeCB.addItem("rp4","rp4")
        self.typeCB.addItem("rp5","rp5")
        self.typeCB.addItem("cm4","cm4")
        self.typeCB.addItem("cm4","cm4")
        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.typeCB)

        self.label_6 = QLabel(self.formLayoutWidget)
        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_6)

        self.roleCB = QComboBox(self.formLayoutWidget)
        self.roleCB.addItem("master","master")
        self.roleCB.addItem("node","node")
        self.roleCB.addItem("storrage","storrage")
        self.roleCB.addItem("single","single")
        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.roleCB)

        self.setWindowTitle(self.title)
        self.label_4.setText("Os")
        self.label_5.setText("typ")
        self.label_6.setText("rolle")
        self.buttonBox.accepted.connect(self.addNewNode)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.buttonBox.close)
       
    def addNewNode(self):
        newName = self.nameEdit.text()
        newNodeJson = {"name": self.nameEdit.text(), "ip": self.ipEdit.text(),"network": str(self.networkCB.currentText()),"os": str(self.osCB.currentText()),"typ": str(self.typeCB.currentText()),"rolle": str(self.roleCB.currentText())}
        nodeArr = self.model.getNodeArry()
        for node in nodeArr:
            if node['name'] == newName:
                self.model.removeNode(node)
        self.model.addNode(newNodeJson)
        self.accept()

    def fillNode(self, node):
        self.nameEdit.setText(node['name'])
        self.ipEdit.setText(node['ip'])
        self.networkCB.setCurrentText(node['network'])
        self.osCB.setCurrentText(node['os'])
        self.typeCB.setCurrentText(node['typ'])
        self.roleCB.setCurrentText(node['rolle'])