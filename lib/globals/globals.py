from PyQt5 import QtWidgets
from struct import Struct

### Globals
PORT = 65432  # Port to listen on
HOST = "127.0.0.1" # Host address
BUFSIZE = 1024
RESERVED_TIMEOUT = 6000 # Timelimit for reservations [ms]
CONNECTION_STATUS_QUERY = 5000 # Ask all 5secs if connection to server is there [ms]
RETRY_CONNECTION = 15 # Time until new connection attempt [s]

### DEFINE TOPICS
TOPIC_ID = 0
TOPIC_START = 1
TOPIC_STOP = 2
TOPIC_PRICE = 3
TOPIC_SOC = 4
TOPIC_ACCU_POWER = 5
TOPIC_CURRENT_POWER = 6
TOPIC_RESERVE = 7
TOPIC_FREE_RESERVE = 8

# Msg Structs: ['Topic' | 'Charge Point' | ('Data') | 'LF']
MSG_ID = Struct('ii8sc')
MSG_START = Struct('iic')
MSG_STOP = Struct('iic')
MSG_PRICE = Struct('iifc')
MSG_SOC = Struct('iifc')
MSG_ACCU_POWER = Struct('iifc')
MSG_CURRENT_POWER = Struct('iifc')
MSG_RESERVE = Struct('ii8sc')
MSG_FREE_RESERVE = Struct('iic')

### DEFINE BUTTON COLORS
BTN_BG_COLOR_NORMAL = "rgb(49, 119, 255)"
BTN_BGS_COLOR_NORMAL = "rgb(75, 136, 255)"
BTN_BG_COLOR_OCCUPY = "rgb(224, 40, 49)"

def setButtonColor(button: QtWidgets.QPushButton, bgs_color=None, bg_color=None):
    """ Sets button bg-color. """
    button.setStyleSheet(f"selection-background-color: {bgs_color}; background-color: {bg_color}")