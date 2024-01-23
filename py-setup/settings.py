from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFormLayout, QLabel, QLineEdit,
    QSizePolicy, QTextEdit, QWidget)
from nodemodel import NodeModel
from config import *

class SettingDlg(QDialog):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.resize(400, 330)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(30, 280, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.formLayoutWidget = QWidget(self)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(10, 10, 381, 261))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.firstuserLbl = QLabel(self.formLayoutWidget)
        self.firstuserLbl.setObjectName(u"firstuserLbl")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.firstuserLbl)

        self.firstuserEdit = QLineEdit(self.formLayoutWidget)
        self.firstuserEdit.setObjectName(u"firstuserEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.firstuserEdit)

        self.passwdLbl = QLabel(self.formLayoutWidget)
        self.passwdLbl.setObjectName(u"passwdLbl")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.passwdLbl)

        self.passwdEdit = QLineEdit(self.formLayoutWidget)
        self.passwdEdit.setObjectName(u"passwdEdit")
        self.passwdEdit.setEchoMode(QLineEdit.Password)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.passwdEdit)

        self.gatewayLbl = QLabel(self.formLayoutWidget)
        self.gatewayLbl.setObjectName(u"gatewayLbl")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.gatewayLbl)

        self.gatewayEdit = QLineEdit(self.formLayoutWidget)
        self.gatewayEdit.setObjectName(u"gatewayEdit")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.gatewayEdit)

        self.ip_maskLbl = QLabel(self.formLayoutWidget)
        self.ip_maskLbl.setObjectName(u"ip_maskLbl")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.ip_maskLbl)

        self.ip_maskCB = QComboBox(self.formLayoutWidget)
        self.ip_maskCB.addItem(u"16")
        self.ip_maskCB.addItem(u"24")
        self.ip_maskCB.setObjectName(u"ip_maskCB")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.ip_maskCB)

        self.nameserversLbl = QLabel(self.formLayoutWidget)
        self.nameserversLbl.setObjectName(u"nameserversLbl")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.nameserversLbl)

        self.nameserversEdit = QLineEdit(self.formLayoutWidget)
        self.nameserversEdit.setObjectName(u"nameserversEdit")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.nameserversEdit)

        self.domainLbl = QLabel(self.formLayoutWidget)
        self.domainLbl.setObjectName(u"domainLbl")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.domainLbl)

        self.domainEdit = QLineEdit(self.formLayoutWidget)
        self.domainEdit.setObjectName(u"domainEdit")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.domainEdit)

        self.ssh_rsaLbL = QLabel(self.formLayoutWidget)
        self.ssh_rsaLbL.setObjectName(u"ssh_rsaLbL")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.ssh_rsaLbL)

        self.ssh_rsaEdit = QTextEdit(self.formLayoutWidget)
        self.ssh_rsaEdit.setObjectName(u"ssh_rsaEdit")

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.ssh_rsaEdit)

        self.setWindowTitle( u"Settings")
        self.firstuserLbl.setText( u"Default User")
        self.passwdLbl.setText( u"Password")
        self.gatewayLbl.setText( u"Gateway")
        self.ip_maskLbl.setText( u"IP-Mask")

        self.nameserversLbl.setText( u"Nameserver")
        self.domainLbl.setText( u"Domain")
        self.ssh_rsaLbL.setText( u"ssh_rsa")
#################################################
        settings = self.model.getSettings()
        self.firstuserEdit.setText(settings['firstuser']) 

        self.passwdEdit.setText( settings['passwd'])

        self.gatewayEdit.setText( settings['gateway'])
        self.ip_maskCB.setCurrentText(settings['ip_mask'])
        self.nameserversEdit.setText( str(settings['nameservers']))
        self.domainEdit.setText(settings['domain'])
        self.ssh_rsaEdit.setText(settings['ssh_rsa'])

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
