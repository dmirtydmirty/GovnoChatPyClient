import socket
import json
from queue import Queue
from threading import Thread
from time import sleep


class TCPClient:
    def __init__(self, msgQueue: Queue):
        self.msgQueue = msgQueue
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cfgFile = "srv.json"
        with open('srv.json', 'r') as file:
            data = json.load(file)
            self.ip = data["host"]
            self.port = data["port"]
        self.active: bool() = False

    def start(self):
        self.sock.connect((self.ip, self.port))
        self.active = True

        msg = json.dumps({"Type": 1, "Sender": 0, "Content": " "}) + "\n\r"

        print(msg)
        self.sock.sendall(msg.encode("UTF-8"))
        print("Client started")
        Thread(target=self.__receive,  daemon=True).start()

    def __receive(self):
        while self.active:
            data = self.sock.recv(1024)
            print("RCV: ", data.decode())
            self.msgQueue.put(data.decode(), block=True)

    def send(self, msg: str):

        self.sock.sendall(msg.encode("UTF-8"))
