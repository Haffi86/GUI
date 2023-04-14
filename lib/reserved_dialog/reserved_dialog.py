from PyQt5.QtWidgets import QWidget, QDesktopWidget
from PyQt5 import QtCore
from ui.reserved import Ui_Reserved

class ReservedDialog(QWidget):
    #Init Function
    def __init__(self, login):
        super().__init__()
        self.reservedUi = Ui_Reserved()
        self.reservedUi.setupUi(self)
        self.login = login
        self.center()
        self.setCursor(QtCore.Qt.BlankCursor)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.reservedUi.btn_back.clicked.connect(self.backButton)

    def center(self):
        self.qr = self.frameGeometry()
        self.cp = QDesktopWidget().availableGeometry().center()
        self.qr.moveCenter(self.cp)
        self.move(self.qr.topLeft())

    def backButton(self):
        self.login.show()
        self.hide()
