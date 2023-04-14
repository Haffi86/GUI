from PyQt5.QtWidgets import QWidget, QDesktopWidget
from PyQt5 import QtCore
from ui.checkoutWidgetLayout import Ui_checkoutWidgetLayout

class CheckoutDialog(QWidget):
    """
    The CheckoutDialog class is a subclass of QWidget and is used to create a custom dialog window
    for the checkout process. It handles the user interaction to either confirm or deny stopping the
    loading process.
    """

    def __init__(self, loading_window):
        """
        Initialize the CheckoutDialog with the provided loading_window object.

        :param loading_window: The parent window (MainWidget) that handles the loading process.
        """
        super().__init__()
        self.checkoutUi = Ui_checkoutWidgetLayout()
        self.checkoutUi.setupUi(self)
        self.center()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        #self.setCursor(Qt.BlankCursor)

        self.windowObj = loading_window

        # Connections
        self.checkoutUi.btn_yes.clicked.connect(self.yesButton)
        self.checkoutUi.btn_no.clicked.connect(self.noButton)

    def center(self):
        """
        Center the CheckoutDialog on the screen.
        """
        self.qr = self.frameGeometry()
        self.cp = QDesktopWidget().availableGeometry().center()
        self.qr.moveCenter(self.cp)
        self.move(self.qr.topLeft())

    def yesButton(self, event):
        """
        Handle the 'Yes' button click event. It hides the dialog, stops the loading process,
        and calls the checkout method from the parent window.

        :param event: The event object passed by the 'Yes' button click signal.
        """
        self.hide()
        self.windowObj.checkout()

    def noButton(self, event):
        """
        Handle the 'No' button click event. It hides the dialog and resumes the loading process
        by restarting the timer.

        :param event: The event object passed by the 'No' button click signal.
        """
        self.hide()
        self.windowObj.timerTimeout.start()