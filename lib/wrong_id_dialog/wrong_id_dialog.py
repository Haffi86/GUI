from PyQt5.QtWidgets import QWidget, QDesktopWidget
from PyQt5 import QtCore
from ui.wrongIDLayout import Ui_wrongIDWidget

class wrongIDDialog(QWidget):

    #Init Function with type hinting
    def __init__(self):
        super().__init__()
        self.wrongIDUi = Ui_wrongIDWidget()
        self.wrongIDUi.setupUi(self)
        self.center()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        #self.setCursor(Qt.BlankCursor)

        #hand over MainWidget object
        self.windowObj = object

        #Connections
        self.wrongIDUi.btn_ok.clicked.connect(self.okButton)

    #centers the Dialog
    def center(self):
        self.qr = self.frameGeometry()
        self.cp = QDesktopWidget().availableGeometry().center()
        self.qr.moveCenter(self.cp)
        self.move(self.qr.topLeft())

    #closes Dialog and opens login
    def okButton(self):
        self.hide()
