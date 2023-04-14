from PyQt5.QtWidgets import QWidget, QDesktopWidget
from PyQt5 import QtCore
from ui.occupied import Ui_Occupied

class OccupedDialog(QWidget):

    #Init Function
    def __init__(self, login):
        super().__init__()
        self.occupiedUi = Ui_Occupied()
        self.occupiedUi.setupUi(self)
        self.login = login
        self.center()
        self.setCursor(QtCore.Qt.BlankCursor)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.occupiedUi.btn_back.clicked.connect(self.backButton)

    def center(self):
        self.qr = self.frameGeometry()
        self.cp = QDesktopWidget().availableGeometry().center()
        self.qr.moveCenter(self.cp)
        self.move(self.qr.topLeft())

    def backButton(self):
        self.login.show()
        self.hide()