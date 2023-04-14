from time import sleep
from pynput import keyboard
import sys


# class RFID_READER():
#     def __init__(self):
#         self.cnt = 0
#         self.arr = []
#         self.string = ""

#     def on_press(self, key):
#         try:
#             print('alphanumeric key {0} pressed'.format(key.char))
#             #self.count(self.cnt, self.arr, key)

#         except AttributeError:
#             print('special key {0} pressed'.format(key))

#     def on_release(key):
#         print('{0} released'.format(key))
#         if key == keyboard.Key.esc:
#             # Stop listener
#             return False

#     def count(self, cnt, arr, key):
#         print("COUNTER: " + str(self.cnt))
#         self.arr.append(key)
#         self.cnt += 1

#         if self.cnt >= 8:
#             print(self.arr)
#             listener.stop()

# rfid_reader = RFID_READER()

# listener = keyboard.Listener(on_press=rfid_reader.on_press)
# listener.start()

# while 1:
#     pass

status = {}
status[0] = "Frei"
status[1] = "Reserviert"
status[2] = "Belegt"

def checkStatus(key):
    

    if status[key] == "Frei":
        print("frei")
    elif status[key] == "Reserviert":
        print("reserviert")
    else:
        print("Belegt")




test = 0

checkStatus(test)


