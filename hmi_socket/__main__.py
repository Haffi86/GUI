from base64 import decode
from lib.globals.globals import *
import socket
import threading
import time

HOST = HOST  # Standard loopback interface address (localhost)
BUFSIZE = 1024

class SocketServer():
    """ SocketServer Class """
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((socket.gethostname(), PORT))
        self.sock.listen(5)

        while True:
            self.conn, self.addr = self.sock.accept()
            print(f"Connected by {self.addr}")
            # Send hello msg to client
            hello = bytes(f"Connected to Server {socket.gethostname()} on port {PORT}", 'UTF-8')
            self.conn.sendall(hello)

            self.thread_recv = threading.Thread(target=self.receive)
            self.thread_recv.start()

            self.thread_reserve = threading.Thread(target=self.sendReserve)
            self.thread_reserve.start()

    def receive(self):
        while True:
            rec = self.conn.recv(BUFSIZE)

            # Trenne den Bytestream am \n (0x0A)
            split_bytestream = rec.split(b'\n')
            # Entferne den letzten leeren Eintrag, falls vorhanden
            # if not split_bytestream[-1]:
            #     split_bytestream.pop()

            # Gib die aufgeteilten Bytestreams aus
            for idx, bs in enumerate(split_bytestream):
                print(f"Teil {idx + 1}: {bs}")

                if len(bs) == 0:
                    break

                # Add '\n' for unpacking data
                bs = bs + b'\n'

                topic = bs[0]
                charge_point = bs[4]

                if topic == TOPIC_ID:
                    data = MSG_ID.unpack(bs)

                    id = data[2]
                    print(f"Got ID: {id} from Charge Point: {charge_point}")

                elif topic == TOPIC_START:
                    print(f"Charging startet from Charge Point: {charge_point}")
                    if charge_point == 1:
                        # Start to send loading info for point 1 to GUI
                        print("Start sending Thread 0")
                        self.thread_charge_point_0 = threading.Thread(target=self.sendToPoint0)
                        self.thread_charge_point_0.start()
                    elif charge_point == 2:
                        # Start to send loading info for point 1 to GUI
                        print("Start sending Thread 1")
                        self.thread_charge_point_1 = threading.Thread(target=self.sendToPoint1)
                        self.thread_charge_point_1.start()
                    elif charge_point == 3:
                        # Start to send loading info for point 1 to GUI
                        print("Start sending Thread 2")
                        self.thread_charge_point_2 = threading.Thread(target=self.sendToPoint2)
                        self.thread_charge_point_2.start()
                    elif charge_point == 4:
                        # Start to send loading info for point 1 to GUI
                        print("Start sending Thread 3")
                        self.thread_charge_point_3 = threading.Thread(target=self.sendToPoint3)
                        self.thread_charge_point_3.start()

                elif topic == TOPIC_STOP:
                    print(f"Charging stopped from Charge Point: {charge_point}")

                else:
                    print("[INFO]: Unknown topic")

    def sendToPoint0(self):
        index = 1
        price = 0.0
        state_of_charge = 0.0
        accu_power = 0
        current_power = 22

        while True:
            # Sending all the loading information every 5s
            self.conn.send(MSG_PRICE.pack(TOPIC_PRICE, index, price, b'\n'))
            self.conn.send(MSG_SOC.pack(TOPIC_SOC, index, state_of_charge, b'\n'))
            self.conn.send(MSG_ACCU_POWER.pack(TOPIC_ACCU_POWER, index, accu_power, b'\n'))
            self.conn.send(MSG_CURRENT_POWER.pack(TOPIC_CURRENT_POWER, index, current_power, b'\n'))
            
            # Emulate data
            price += 0.5
            state_of_charge += 3
            accu_power += 4
            time.sleep(5)

    def sendToPoint1(self):
        index = 2
        price = 0.0
        state_of_charge = 0.0
        accu_power = 0
        current_power = 22

        while True:
            # Sending all the loading information every 5s
            self.conn.send(MSG_PRICE.pack(TOPIC_PRICE, index, price, b'\n'))
            self.conn.send(MSG_SOC.pack(TOPIC_SOC, index, state_of_charge, b'\n'))
            self.conn.send(MSG_ACCU_POWER.pack(TOPIC_ACCU_POWER, index, accu_power, b'\n'))
            self.conn.send(MSG_CURRENT_POWER.pack(TOPIC_CURRENT_POWER, index, current_power, b'\n'))
            
            # Emulate data
            price += 0.5
            state_of_charge += 3
            accu_power += 4
            time.sleep(5)

    def sendToPoint2(self):
            index = 3
            price = 0.0
            state_of_charge = 0.0
            accu_power = 0
            current_power = 22

            while True:
                # Sending all the loading information every 5s
                self.conn.send(MSG_PRICE.pack(TOPIC_PRICE, index, price, b'\n'))
                self.conn.send(MSG_SOC.pack(TOPIC_SOC, index, state_of_charge, b'\n'))
                self.conn.send(MSG_ACCU_POWER.pack(TOPIC_ACCU_POWER, index, accu_power, b'\n'))
                self.conn.send(MSG_CURRENT_POWER.pack(TOPIC_CURRENT_POWER, index, current_power, b'\n'))
                
                # Emulate data
                price += 0.5
                state_of_charge += 3
                accu_power += 4
                time.sleep(5)

    def sendToPoint3(self):
            index = 4
            price = 0.0
            state_of_charge = 0.0
            accu_power = 0
            current_power = 22

            while True:
                # Sending all the loading information every 5s
                self.conn.send(MSG_PRICE.pack(TOPIC_PRICE, index, price, b'\n'))
                self.conn.send(MSG_SOC.pack(TOPIC_SOC, index, state_of_charge, b'\n'))
                self.conn.send(MSG_ACCU_POWER.pack(TOPIC_ACCU_POWER, index, accu_power, b'\n'))
                self.conn.send(MSG_CURRENT_POWER.pack(TOPIC_CURRENT_POWER, index, current_power, b'\n'))
                
                # Emulate data
                price += 0.5
                state_of_charge += 3
                accu_power += 4
                time.sleep(5)

    def sendReserve(self):
        time.sleep(3)
        id = bytes('12341234', 'utf-8')
        charge_point = 1
        self.conn.send(MSG_RESERVE.pack(TOPIC_RESERVE, charge_point, id, b'\n'))
        time.sleep(100)
        self.conn.send(MSG_FREE_RESERVE.pack(TOPIC_FREE_RESERVE, charge_point, b'\n'))


socker_server = SocketServer()