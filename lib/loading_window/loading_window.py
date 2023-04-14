from PyQt5.QtWidgets import QWidget
from PyQt5 import QtGui, QtCore
from lib.globals.globals import *
import time

#TODO: evtl UI_Main umbenennen
from lib.checkout_dialog.checkout_dialog import CheckoutDialog
from ui.main import Ui_Main

class LoadingWindow(QWidget):

    def __init__(self, index, login, button):
        #Build GUI from QT
        super().__init__()
        self.MainUi = Ui_Main()
        self.MainUi.setupUi(self)
        #self.setCursor(Qt.BlankCursor)
        
        self.login = login
        self.button = button
        self.checkoutDialog = CheckoutDialog(self)

        #Style Contents
        #self.MainUi.btn_input.setStyleSheet("border: 2px solid white; border-radius: 7px")
        #self.setStyleSheet("color: white; background-color: rgb(106, 233, 255);")
        self.MainUi.l_battery.setStyleSheet("border: 2px solid white; border-radius: 7px; color: orange;")
        self.MainUi.l_deliveredPower.setStyleSheet("border: 2px solid white; border-radius: 7px; color: orange;")
        self.MainUi.l_currentPower.setStyleSheet("border: 2px solid white; border-radius: 7px; color: orange;")
        #self.MainUi.btn_stop.setStyleSheet("color: white; background-color: rgb(37, 150, 220); border: 2px solid white; border-radius: 7px")

        #Init other stuff
        self.MainUi.lcd_duration.display("00:00:00")
        self.MainUi.lcd_estimation.display("00:00")
        self.MainUi.l_station.setText(str(index))
        self.MainUi.l_batteryImage.setPixmap(QtGui.QPixmap("./ui/Bilder/akku_0.png"))

        #Init Date/Time and TimeoutTimer
        self.timerDate = QtCore.QTimer()
        self.timerDate.timeout.connect(self.setDate)
        self.timerDate.start(1000)

        # timeout-timer, that sends us back to login window
        self.timerTimeout = QtCore.QTimer()
        self.timerTimeout.timeout.connect(self.showLogin)

        #Connections
        #self.MainUi.btn_stop.clicked.connect(self.mainButton)
        self.MainUi.btn_stop.mouseReleaseEvent = self.mainButton

        self.MainUi.btn_start.clicked.connect(self.startProcess)
        # self.MainUi.l_chargeStatus.mouseReleaseEvent = self.startProcess

        #self.MainUi.l_batteryImage.mouseReleaseEvent = self.checkoutAsk

        #self.MainUi.l_batteryImage.mouseReleaseEvent = self.checkout
        # self.MainUi.l_batteryImage.mouseReleaseEvent = self.checkoutAsk
        

        #Create Variables
        self.state_of_charge = 0
        self.accumulated_power = 0
        self.current_power = 0
        self.toggle = 0
        self.price = 0
        self.index = index

        self.running = False

        self.status = "Frei"
        self.ID = ""

        #Set Labels
        self.MainUi.l_battery.setText(str(self.state_of_charge) + " %")
        self.MainUi.l_deliveredPower.setText(str(self.accumulated_power) + " kWh")
        self.MainUi.l_price.setText(str(self.price) + " €")
        self.MainUi.l_currentPower.setText(str(self.current_power) + " kW")

    def updateDisplay(self):
        print("DEBUG: update display")
        self.MainUi.l_battery.setText(str(self.state_of_charge) + " %")
        self.MainUi.l_deliveredPower.setText(str(self.accumulated_power) + " kWh")
        self.MainUi.l_price.setText(str(self.price) + " €")
        self.MainUi.l_currentPower.setText(str(self.current_power) + " kW")

    #Get current Date und Time
    def setDate(self):
        self.MainUi.l_time.setText(QtCore.QTime.currentTime().toString("hh:mm"))
        self.MainUi.l_date.setText(QtCore.QDate.currentDate().toString("dd.MM.yyyy"))

    #show window in Fullscreen and start Timer for Timeout
    def showFull(self):
        """ Show loading winodw fullscreen and start timeout-timer """
        self.showFullScreen()
        self.timerTimeout.start(20000) # 60000ms -> 1min

    #go back to login window
    def showLogin(self):
        """ When timeout-timer runs out, go back to login screen -> Prevent staying in loading-window forever. """
        self.hide()
        self.login.showFullScreen()
        self.timerTimeout.stop()
        

    #Stop Button action, check ID with authWindow first
    def stopButton(self, event):
        self.login.auth.showFull("stop")
        self.timerTimeout.stop()

    #Resume Button action, check ID with authWindow first
    def resumeButton(self, event):
        self.login.auth.showFull("resume")
        self.timerTimeout.stop()

    #Ask customer, before checkout
    def checkoutAsk(self, event):
        self.login.auth.showFull("checkout")
        self.timerTimeout.stop()

    def mainButton(self, event):
        self.login.show()
        self.hide()

    #Input Button action
    def inputButton(self, event):
        # self.capacity = 123
        # self.state_of_charge = 12

        # self.totalLoad = self.capacity * (self.state_of_charge / 100)
        # self.current_power = 22

        #TODO:evtl estimated time einbauen, frage obs nötig ist?
        #calculate estimated time based on
        # self.difference = self.capacity - self.totalLoad
        # temp = self.difference / self.current_power
        # tempHour = int(temp)
        # tempMin = int((temp - tempHour) * 60)
        # print("Time Left: " + str(temp))
        # print("Stunde: " + str(tempHour))
        # print("Minute: " + str(tempMin))
        #self.MainUi.lcd_estimation.display(str('0')+":"+str('0')+":00")

        # self.MainUi.l_currentPower.setText(str(self.current_power) + " kW")
        # self.MainUi.l_deliveredPower.setText(str(0))
        # self.accumulated_power = 0

        self.startProcess()

    def startProcess(self):
        """ Start loading process. Fully occupy station. """
        self.MainUi.btn_start.setVisible(False)
        # Create 1sec interval timer: for loading duration
        self.time = QtCore.QTime(0, 0, 0)
        self.timerSec = QtCore.QTimer()
        self.timerSec.timeout.connect(self.countTime)
        self.timerSec.start(1000)

        # Update display
        self.updateDisplayTimer = QtCore.QTimer()
        self.updateDisplayTimer.timeout.connect(self.updateDisplay)
        self.updateDisplayTimer.start(5000)
        
        # Create 600ms interval timer: for blinking battery
        self.timerBlink = QtCore.QTimer()
        self.timerBlink.timeout.connect(self.blink)
        self.timerBlink.start(600)

        #Set occupied status and switch button
        self.status = "Belegt"
        self.running = True
        self.MainUi.btn_stop.setText("Checkout")
        self.MainUi.l_chargeStatus.setPixmap(QtGui.QPixmap("./ui/Bilder/car_lock.png"))
        self.MainUi.btn_stop.mouseReleaseEvent = self.checkoutAsk
        setButtonColor(self.button, None, BTN_BG_COLOR_OCCUPY)

        # Send info to socket
        self.login.socket.send(MSG_ID.pack(TOPIC_ID, self.index, bytes(self.ID, 'utf-8'), b'\n'))
        self.login.socket.send(MSG_START.pack(TOPIC_START, self.index, b'\n'))
        print(f"DEBUG: sending start command from index {self.index}")

    #1-Sec Interval: count loading duration
    def countTime(self):
        self.time = self.time.addSecs(1)
        self.MainUi.lcd_duration.display(self.time.toString('hh:mm:ss'))
        # self.login.socket.send(MSG_ID.pack(TOPIC_DURATION, self.index, bytes(self.time.toString('hh:mm:ss'), 'utf-8')))

        self.price = round(self.accumulated_power * 0.35, 2)
        self.MainUi.l_price.setText(str(self.price) + " €")

    def blink(self):
        self.controlBattery()
        self.MainUi.l_battery.setText(str(self.state_of_charge) + " %")

    def controlBattery(self):
        battery_ranges = [
            (0, 20, "./ui/Bilder/akku_0.png", "./ui/Bilder/akku_0-20.png"),
            (20, 40, "./ui/Bilder/akku_20.png", "./ui/Bilder/akku_20-40.png"),
            (40, 60, "./ui/Bilder/akku_40.png", "./ui/Bilder/akku_40-60.png"),
            (60, 80, "./ui/Bilder/akku_60.png", "./ui/Bilder/akku_60-80.png"),
            (80, 100, "./ui/Bilder/akku_80.png", "./ui/Bilder/akku_80-100.png"),
        ]

        for lower, upper, img1, img2 in battery_ranges:
            if lower <= self.state_of_charge < upper:
                self.update_battery_image(img1 if self.toggle == 0 else img2)
                break
        else:
            self.MainUi.l_batteryImage.setPixmap(QtGui.QPixmap("./ui/Bilder/akku_80-100.png"))
            self.state_of_charge = 100
            self.finishProcess()

    def update_battery_image(self, image_path: str):
            self.MainUi.l_batteryImage.setPixmap(QtGui.QPixmap(image_path))
            self.toggle = not self.toggle

    #end process
    def finishProcess(self):
        """ Stop timer and set running flag to False to indicate loading process is not active. """
        self.running = False

        self.timerSec.stop()
        self.timerBlink.stop()

        #self.MainUi.l_chargeStatus.setPixmap(QtGui.QPixmap("car_unlock.png"))
        self.MainUi.btn_stop.setText("Checkout")
        #self.MainUi.btn_stop.clicked.disconnect()
        #self.MainUi.btn_stop.clicked.connect(self.checkout)

        self.MainUi.btn_stop.mouseReleaseEvent = self.checkoutAsk

    #adapt ui to stop charging
    def stopCharge(self):
        self.running = False
        #stop timers
        self.timerSec.stop()
        self.timerBlink.stop()

        self.MainUi.l_chargeStatus.setPixmap(QtGui.QPixmap("./ui/Bilder/car_unlock.png"))
        self.MainUi.btn_stop.setText("Ladevorgang fortsetzen")
        #self.MainUi.btn_stop.clicked.disconnect()
        #self.MainUi.btn_stop.clicked.connect(self.resumeButton)

        self.MainUi.btn_stop.mouseReleaseEvent = self.resumeButton

    #adapt ui to resume charging
    def resumeCharge(self):
        self.running = True
        self.MainUi.l_chargeStatus.setPixmap(QtGui.QPixmap("./ui/Bilder/car_lock.png"))
        self.MainUi.btn_stop.setText("Ladevorgang stoppen")
        #self.MainUi.btn_stop.clicked.disconnect()
        #self.MainUi.btn_stop.clicked.connect(self.stopButton)

        self.MainUi.btn_stop.mouseReleaseEvent = self.stopButton

    	#start timers again
        self.timerSec.start(1000)
        self.timerBlink.start(800)

    #check out customer, reset all
    def checkout(self):
        """ Checkout customer.  """
        #stop process if its still running
        if self.running == True:
            self.finishProcess()

        self.MainUi.l_chargeStatus.setPixmap(QtGui.QPixmap("./ui/Bilder/car_unlock.png"))

        self.status = "Frei"
        self.ID = ""
        self.login.socket.send(MSG_STOP.pack(TOPIC_STOP, self.index, b'\n'))

        if self.index == 1:
            setButtonColor(self.login.loginUi.btn_station1, None, BTN_BG_COLOR_NORMAL)
        elif self.index == 2:
            setButtonColor(self.login.loginUi.btn_station2, None, BTN_BG_COLOR_NORMAL)
        elif self.index == 3:
            setButtonColor(self.login.loginUi.btn_station3, None, BTN_BG_COLOR_NORMAL)
        else:
            setButtonColor(self.login.loginUi.btn_station4, None, BTN_BG_COLOR_NORMAL)

        self.state_of_charge = 0
        self.accumulated_power = 0
        self.current_power = 0
        self.totalLoad = 0
        self.toggle = 0
        self.price = 0
        self.time = QtCore.QTime(0, 0, 0)
        self.updateDisplayTimer.stop()

        self.MainUi.l_battery.setText(str(self.state_of_charge) + " %")
        self.MainUi.l_deliveredPower.setText(str(self.accumulated_power) + " kWh")
        self.MainUi.l_currentPower.setText(str(self.current_power) + " kW")
        self.MainUi.lcd_duration.display(self.time.toString("hh:mm:ss"))
        self.MainUi.l_price.setText(str(self.price) + " €")
        self.MainUi.l_batteryImage.setPixmap(QtGui.QPixmap("./ui/Bilder/akku_0.png"))

        self.MainUi.btn_stop.setText("Zurück")
        self.MainUi.btn_stop.mouseReleaseEvent = self.mainButton
        self.MainUi.btn_start.setVisible(True)
        
        self.hide()
        self.login.show()