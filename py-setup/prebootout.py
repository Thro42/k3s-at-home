import os, string
from ctypes import windll
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,QCheckBox,
    QDialogButtonBox, QFormLayout, QLabel, QSizePolicy,
    QWidget)
from ubuntu import UbuntuSettings
from config import *

class PreBootOut(QDialog):
    def __init__(self, parent, model):
        super().__init__(parent)
        self.model = model
        self.resize(292, 166)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 120, 271, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.formLayoutWidget = QWidget(self)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(10, 20, 261, 91))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.driveLbl = QLabel(self.formLayoutWidget)
        self.driveLbl.setObjectName(u"driveLbl")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.driveLbl)

        self.driveCB = QComboBox(self.formLayoutWidget)
        self.driveCB.setObjectName(u"driveCB")

        bitmask = windll.kernel32.GetLogicalDrives()
        print(bitmask)
        letter = ord('A')
        while bitmask > 0:
            if bitmask & 1:
                if chr(letter) != 'C':
                    print(letter)
                    drv = chr(letter) + ':\\'
                    self.driveCB.addItem(drv,drv)
            bitmask >>= 1
            letter += 1
#            bitmask >>= 1

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.driveCB)

        self.label = QLabel(self.formLayoutWidget)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.comboBox = QComboBox(self.formLayoutWidget)
        self.comboBox.setObjectName(u"comboBox")
        nodeArr = self.model.getNodeArry()
        for node in nodeArr:
            self.comboBox.addItem(node['name'],node['name'])

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.comboBox)

        self.cbNetwork = QCheckBox(self.formLayoutWidget)
        self.cbNetwork.setObjectName(u"cbNetwork")
        self.cbNetwork.setText(u"Network Data")
        self.cbNetwork.setChecked(True)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.cbNetwork)

        self.cbUser = QCheckBox(self.formLayoutWidget)
        self.cbUser.setObjectName(u"cbUser")
        self.cbUser.setText(u"User Data")
        self.cbUser.setChecked(True)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.cbUser)
        self.buttonBox.accepted.connect(self.acceptSelection)
        self.buttonBox.rejected.connect(self.reject)

    def acceptSelection(self):
        theDrive = self.driveCB.currentText()
        theNode =  self.comboBox.currentText()
        nodeArr = self.model.getNodeArry()
        for node in nodeArr:
            if node['name'] == theNode:
                 self.prepBootFiles(theDrive, node)
        self.accept()

    def prepBootFiles(self, drive, node):
        print("Drive: ", drive)
        print("Node: ", node['name'])
        print(" OS: ", node['os'])
        if node['os'] == "ubuntu":
            self.prepareUbuntu(drive, node)
        elif node['os'] == "buster":
            print("Perpare firstrun.sh")
        elif node['os'] == "bookworm":
            print("Perpare interfaces")


    def prepareUbuntu(self, drive, node):
        print("Perpare ubuntu")
        settings = self.model.getSettings()
        ubuntu = UbuntuSettings(settings,drive,node)
        if self.cbUser.isChecked() == True:
            print("Perpare user-data")
            ubuntu.save_user_data()
        if self.cbNetwork.isChecked() == True:
            print("Perpare network-config")
            ubuntu.save_net_config()
            print("set IP to:", node['ip'])
