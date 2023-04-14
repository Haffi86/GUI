from PyQt5.QtWidgets import *
from PyQt5 import QtCore

from ui.auth import Ui_AuthWindow

class AuthWindow(QWidget):
    """ AuhtWindow Class handles authentification by scanned RFID. """
    def __init__(self, login):
        """ Constructor, loads UI. """
        # Setup GUI
        super().__init__()
        self.authUi = Ui_AuthWindow()
        self.authUi.setupUi(self)

        # Hand over LoginWindow object
        self.login = login

        # Button Connections
        self.authUi.btn_back.clicked.connect(self.backButton)

        # Variables needed for authentification process
        self.id_list = []
        self.id_string = ""
        self.action = "none"

    def keyPressEvent(self, event):
        """ Process key inputs. """
        print("[INFO]: keyPressEvent from Auth")
        # Shift: ignore 
        if event.key() == QtCore.Qt.Key_Shift:
            pass
        # Tab: input finished
        elif event.key() == QtCore.Qt.Key_Tab:
            # Convert list to string
            self.id_string = "".join(self.id_list)

            # Look if LoadingWindow is visible
            visible_window = None
            for window in [self.login.window0, self.login.window1, self.login.window2, self.login.window3]:
                if window.isVisible():
                    visible_window = window
                    break

            if visible_window:
                self.handle_window(visible_window)
            elif self.login.isVisible():
                if self.action == "take-reserved":
                    self.login.takeReservedExecute(self.id_string)
                else:
                    self.login.checkID(self.charge_point, self.id_string, "belegen")

            self.id_list = []
            self.hide()
        # NOTE: EXIT PROGRAM without needing CTRL+C
        elif chr(event.key()) == 'Q':
            print("Exiting Program")
            exit()
        # Any other key: read input as char and fill list
        else:
            try:
                self.id_list.append(chr(event.key()))
                print(f"[INFO]: ID List = {self.id_list}")
            except:
                print("That was not the right key")

    def handle_window(self, window):
        """ Check if scanned ID matches with deposited ID of visible window. """
        if self.id_string == window.ID and self.action in ["stop", "resume", "checkout"]:
            getattr(window, f"{self.action}Dialog").show()
        else:
            # IDs didn't match -> back to login
            self.login.wrongIDDialog.show()
            self.login.show()
            window.hide()

    def setIndex(self, charge_point):
        """ Set number of charge point. """
        self.charge_point = charge_point

    #show window fullscreen and resize content -> keyPressEvent then takes over
    def showFull(self, action):
        """  """
        #self._pixmap = QtGui.QPixmap(self.authUi.label.pixmap())
        self.showFullScreen()
        self.action = action
        #self.authUi.label.setPixmap(self._pixmap.scaled(self.authUi.label.width(), self.authUi.label.height(), QtCore.Qt.KeepAspectRatio))

    #backButton action
    def backButton(self):
        self.login.show()
        self.hide()
        