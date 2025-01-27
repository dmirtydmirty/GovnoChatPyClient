import tkinter as tk
from tkinter import ttk, DISABLED, NORMAL

import tcpClient
from queue import Queue
from threading import Thread
from json import loads, dumps


class GUI:
    def __init__(self, root):
        self.txt = tk.Text(root, width=60)
        self.txt.grid(row=1, column=0, columnspan=2)
        self.txt.config(state=DISABLED)

        scrollbar = ttk.Scrollbar(orient="vertical", command=self.txt.yview)
        scrollbar.place(relheight=1, relx=0.974)

        self.e = ttk.Entry(root, width=55)
        self.e.bind("<Return>", self.send)
        self.e.grid(row=2, column=0)

        ttk.Button(root, text="Send", command=self.send).grid(row=2, column=1)
        self.queue = Queue()
        self.client = tcpClient.TCPClient(self.queue)
        self.id = self.client.start()
        print("My id: " + str(self.id))
        Thread(target=self.__receive,  daemon=True).start()

    def send(self, event=None):
        if self.e.get() == str():
            return
        textToSend = f"You (User{self.id}) -> " + self.e.get()
        self.__write_messege(textToSend)
        msg = dumps({"Type": 0, "Sender": self.id, "Message": { "Content": str(self.e.get()) } }, indent=4) + "\n\r"
        self.client.send(msg)
        self.e.delete(0, tk.END)

    def __receive(self):
        while True:
            msg: str = self.queue.get()
            msgParsed = loads(msg)
            msgType = msgParsed["Type"]
            if msgType == 0:
                 self.__write_messege(f"User{msgParsed['Sender']} -> {msgParsed['Message']['Content']}")
            if msgType == 2:
                self.__write_messege(msgParsed["Message"]["StatusInfo"])

    def __write_messege(self, msg: str):
        self.txt.config(state=NORMAL)
        self.txt.insert(tk.END, msg + "\n")
        self.txt.config(state=DISABLED)