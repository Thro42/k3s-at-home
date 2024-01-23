import os, string
from ctypes import windll
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFormLayout, QLabel, QSizePolicy,
    QWidget)
from config import *

class PreBootOut(QDialog):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.resize(292, 153)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 100, 271, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.formLayoutWidget = QWidget(self)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(10, 20, 261, 71))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.driveLbl = QLabel(self.formLayoutWidget)
        self.driveLbl.setObjectName(u"driveLbl")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.driveLbl)

        self.driveCB = QComboBox(self.formLayoutWidget)
        self.driveCB.setObjectName(u"driveCB")

        bitmask = windll.kernel32.GetLogicalDrives()
        letter = ord('A')
        while bitmask > 0:
            if bitmask & 1:
                if letter != 'C':
                    drv = chr(letter) + ':\\'
                    self.driveCB.addItem(drv,drv)
            bitmask >>= 1
            letter += 1
            bitmask >>= 1

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
            self.prepareUbuntu(self, drive, node)
        elif node['os'] == "buster":
            print("Perpare firstrun.sh")
        elif node['os'] == "bookworm":
            print("Perpare interfaces")

        print("set IP to:", node['ip'])

    def prepareUbuntu(self, drive, node):
        print("Perpare ubuntu")
        print("Perpare network-config")
