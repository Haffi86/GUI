from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore
from ui.reserveLayout import Ui_ReserveLayout

class ReserveDialog(QDialog):

    #Init Function with type hinting
    def __init__(self, login):
        super().__init__()
        self.reserveUi = Ui_ReserveLayout()
        self.reserveUi.setupUi(self)
        self.login = login
        self.setCursor(QtCore.Qt.BlankCursor)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.reserveUi.btn_enter.clicked.connect(self.enterButton)


    def enterButton(self):
        self.login.show()
        self.hide()