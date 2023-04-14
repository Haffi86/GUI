import sys
import socket
import time

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ui.login import Ui_LoginWindow
from lib.auth.auth_util import AuthWindow
from lib.reserved_dialog.reserved_dialog import ReservedDialog
from lib.occupied_dialog.occupied_dialog import OccupedDialog
from lib.wrong_id_dialog import wrongIDDialog
from lib.reserve_dialog.reserve_dialog import ReserveDialog
from lib.loading_window.loading_window import LoadingWindow
from lib.globals.globals import *

class LoginWindow(QWidget):
    """ LoginWindow Class, is start screen of GUI. Manages whole GUI application. """
    def __init__(self):
        """ Constructor, loads UI, establishes socket-client and sets up other window-instances. """
        # Setup GUI
        super().__init__()
        self.loginUi = Ui_LoginWindow()
        self.loginUi.setupUi(self)
        #self.setCursor(Qt.BlankCursor)
        self.showFullScreen()

        # Setup Socket Client and start connecting
        self.socket = SocketClient(self)
        self.socket_connect = QThread()
        self.socket.moveToThread(self.socket_connect)
        self.socket_connect.started.connect(self.socket.connect)
        self.socket_connect.start()

        # Connect charge-point buttons to respective authentication-function
        self.loginUi.btn_station1.clicked.connect(lambda: self.startAuthentication(1))
        self.loginUi.btn_station2.clicked.connect(lambda: self.startAuthentication(2))
        self.loginUi.btn_station3.clicked.connect(lambda: self.startAuthentication(3))
        self.loginUi.btn_station4.clicked.connect(lambda: self.startAuthentication(4))

        # Set default charge-point button style
        setButtonColor(self.loginUi.btn_station1, BTN_BGS_COLOR_NORMAL, BTN_BG_COLOR_NORMAL)
        setButtonColor(self.loginUi.btn_station2, BTN_BGS_COLOR_NORMAL, BTN_BG_COLOR_NORMAL)
        setButtonColor(self.loginUi.btn_station3, BTN_BGS_COLOR_NORMAL, BTN_BG_COLOR_NORMAL)
        setButtonColor(self.loginUi.btn_station4, BTN_BGS_COLOR_NORMAL, BTN_BG_COLOR_NORMAL)

        # Set NoFocus on buttons to prevent 'tabulators being eaten'
        self.loginUi.btn_station1.setFocusPolicy(Qt.ClickFocus | Qt.NoFocus)
        self.loginUi.btn_station2.setFocusPolicy(Qt.ClickFocus | Qt.NoFocus)
        self.loginUi.btn_station3.setFocusPolicy(Qt.ClickFocus | Qt.NoFocus)
        self.loginUi.btn_station4.setFocusPolicy(Qt.ClickFocus | Qt.NoFocus)

        # Create instances for other windows/dialoges
        self.auth = AuthWindow(self)
        self.window0 = LoadingWindow(1, self, self.loginUi.btn_station1)
        self.window1 = LoadingWindow(2, self, self.loginUi.btn_station2)
        self.window2 = LoadingWindow(3, self, self.loginUi.btn_station3)
        self.window3 = LoadingWindow(4, self, self.loginUi.btn_station4)
        self.occupiedDialog = OccupedDialog(self)
        self.reservedDialog = ReservedDialog(self)
        self.reserveDialog = ReserveDialog(self)
        self.wrongIDDialog = wrongIDDialog()

        # Timer
        self.timerUpdateConn = QtCore.QTimer()
        self.timerUpdateConn.timeout.connect(self.updateConnStatus)
        self.timerUpdateConn.start(CONNECTION_STATUS_QUERY)

        # Variables needed for login process
        self.id_list = []
        self.id_string = ""
        
    def updateConnStatus(self):
        """ Update the status of connection to server. """
        if self.socket.getConnStatus():
            self.loginUi.server_status.setText("Connected")
        else:
            self.loginUi.server_status.setText("No Conn")

    def keyPressEvent(self, event):
        """ Catch key inputs and try to take a reserved station by comparing deposited ID. """
        print("[INFO]: keyPressEvent from Main")
        # Ignore input 'Shifts'
        if event.key() == QtCore.Qt.Key_Shift:
            pass
        # Finish input on 'Tab'
        elif event.key() == QtCore.Qt.Key_Tab:
            self.id_string = ""
            self.id_string = self.id_string.join(self.id_list)
            # hide only when user reserved a station
            if login.takeReservedExecute(self.id_string):
                self.hide()
            self.id_list = []
        # Read other keys as 'char' and fill list
        else:
            try:
                self.id_list.append(chr(event.key()))
                print(f"[INFO]: ID List = {self.id_list}")
            except:
                print("That was not the right key")

    def reserve(self, charge_point, id):
        """ Reserve a charge point and deposit the ID."""
        id = id.decode('utf-8')
        self.checkID(charge_point, id, "reservieren")

    def takeReservedExecute(self, scanned_id):
        """ Checks if ID assigned to window matches the scanned ID.
            Return False when no match.
            Return True when match. """
        if self.window0.ID == scanned_id:
            login.checkID(1, scanned_id, "belegen")
        elif self.window1.ID == scanned_id:
            login.checkID(2, scanned_id, "belegen")
        elif self.window2.ID == scanned_id:
            login.checkID(3, scanned_id, "belegen")
        elif self.window3.ID == scanned_id:
            login.checkID(4, scanned_id, "belegen")
        else:
            print("[INFO]: Scanned ID did not matched any deposited ID. You didn't reserved a station.")
            return False

        return True

    def freeReserved(self, charge_point, window_obj):
        """ Free reserved station when getting the signal from Server. """

        if charge_point == 1:
            setButtonColor(self.loginUi.btn_station1, BTN_BGS_COLOR_NORMAL, BTN_BG_COLOR_NORMAL)
        elif charge_point == 2:
            setButtonColor(self.loginUi.btn_station2, BTN_BGS_COLOR_NORMAL, BTN_BG_COLOR_NORMAL)
        elif charge_point == 3:
            setButtonColor(self.loginUi.btn_station3, BTN_BGS_COLOR_NORMAL, BTN_BG_COLOR_NORMAL)
        else:
            setButtonColor(self.loginUi.btn_station4, BTN_BGS_COLOR_NORMAL, BTN_BG_COLOR_NORMAL)

        window_obj.ID = ""
        window_obj.status = "Frei"
        print(f"[INFO]: Reservation of station-{charge_point} was removed, cause reservation-time ran out.")

    def startAuthentication(self, charge_point):
        """ Start authentication process by setting index and show auth-window. """
        self.auth.setIndex(charge_point)
        self.auth.showFull('none')

    def checkID(self, index, ID, action):
        if index == 0:
            print("all stations occupied")
            return

        windows = [self.window0, self.window1, self.window2, self.window3]
        buttons = [self.loginUi.btn_station1, self.loginUi.btn_station2, self.loginUi.btn_station3, self.loginUi.btn_station4]

        window = windows[index - 1]
        button = buttons[index - 1]

        if action == "reservieren":
            if window.status == "Frei":
                window.ID = ID
                button.setStyleSheet("background-color: rgb(252, 186, 3)")
                window.status = "Reserviert"
            else:
                self.occupiedDialog.show()
                print(f"Station {index} is already reserved/occupied by another person")

        else:
            if window.status == "Frei":
                window.ID = ID
                window.showFull()
                self.hide()
            elif window.status == "Reserviert":
                if window.ID == ID:
                    window.showFull()
                    self.hide()
                else:
                    self.reservedDialog.show()
                    print(f"Station {index} ist bereits von einer anderen Person reserviert, andere versuchen")
            else:
                if window.ID == ID:
                    window.showFull()
                    self.hide()
                else:
                    self.occupiedDialog.show()
                    print(f"Station {index} ist bereits von einer anderen Person belegt")

class SocketClient(QObject):
    """ SocketClient class implements, interface to SocketServer. Is a child of QObject so it can
        be moved to a QThread.  """
    def __init__(self, login: LoginWindow):
        """ Constructor, set intern variables and hand 'login-window' object over. """
        super().__init__()
        self.host = HOST
        self.port = PORT
        self.BUFSIZE = BUFSIZE
        self.is_connected = False
        self.login = login

    def connect(self):
        """ Connect is executed as Thread when LoginWindow class is called. When connecting fails, retry after 15s"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.sock.connect((socket.gethostname(), self.port))
            except:
                print("[INFO] Connection got refused. Trying again...")
                time.sleep(RETRY_CONNECTION)
            else:
                print("[INFO]: Connection to server established")
                self.is_connected = True
                self.socket_listen = QThread()
                self.moveToThread(self.socket_listen)
                self.socket_listen.started.connect(self.receive)
                self.socket_listen.start()
                break

    def receive(self):
        """ Split received bytestream at '\n' into messages and decide based on TOPIC what to do. """
        while True:
            rec = self.sock.recv(self.BUFSIZE)
            split_bytestream = rec.split(b'\n')

            for _, bs in enumerate(split_bytestream):
                if len(bs) == 0:
                    break

                bs = bs + b'\n'
                topic = bs[0]
                charge_point = bs[4]
                data = None

                if topic == TOPIC_PRICE:
                    data = MSG_PRICE.unpack(bs)
                elif topic == TOPIC_SOC:
                    data = MSG_SOC.unpack(bs)
                elif topic == TOPIC_ACCU_POWER:
                    data = MSG_ACCU_POWER.unpack(bs)
                elif topic == TOPIC_CURRENT_POWER:
                    data = MSG_ACCU_POWER.unpack(bs)
                elif topic == TOPIC_RESERVE:
                    data = MSG_RESERVE.unpack(bs)
                elif topic == TOPIC_FREE_RESERVE:
                    data = MSG_FREE_RESERVE.unpack(bs)
                else:
                    print(f"[INFO]: Unknown topic. Received msg: {rec}")
                    continue

                value = data[2]
                window = getattr(self.login, f"window{charge_point - 1}")

                if topic == TOPIC_PRICE:
                    window.price = value
                elif topic == TOPIC_SOC:
                    window.state_of_charge = round(value, 2)
                elif topic in (TOPIC_ACCU_POWER, TOPIC_CURRENT_POWER):
                    attr_name = "accumulated_power" if topic == TOPIC_ACCU_POWER else "current_power"
                    setattr(window, attr_name, value)
                elif topic == TOPIC_RESERVE:
                    login.reserve(charge_point, value)
                elif topic == TOPIC_FREE_RESERVE:
                    login.freeReserved(charge_point, window)

    def send(self, msg):
        """ Send message to socket. """
        self.sock.send(msg)

    def getConnStatus(self):
        """ Return connection status. """
        return self.is_connected

app = QtWidgets.QApplication(sys.argv)
login = LoginWindow()
login.show()
sys.exit(app.exec())