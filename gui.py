import tkinter as tk
from tkinter import ttk
import tcpClient
from queue import Queue
from threading import Thread


class GUI:
    def __init__(self, root):
        self.txt = tk.Text(root, width=60)
        self.txt.grid(row=1, column=0, columnspan=2)

        scrollbar = ttk.Scrollbar(orient="vertical", command=self.txt.yview)
        scrollbar.place(relheight=1, relx=0.974)

        self.e = ttk.Entry(root, width=55)
        self.e.bind("<Return>", self.send)
        self.e.grid(row=2, column=0)

        ttk.Button(root, text="Send", command=self.send).grid(row=2, column=1)
        self.queue = Queue()
        self.client = tcpClient.TCPClient(self.queue)
        self.client.start()
        Thread(target=self.__receive,  daemon=True).start()

    def send(self, event=None):
        if self.e.get() == str():
            return
        textToSend = "You -> " + self.e.get()
        self.txt.insert(tk.END, textToSend + "\n")
        self.client.send(self.e.get() + "\r\n")
        self.e.delete(0, tk.END)

    def __receive(self):
        while True:
            msg: str = self.queue.get()
            msgParsed = msg.split("///")
            msgType = msgParsed[0]
            if msgType == "USERMSG":
                self.txt.insert(tk.END, msgParsed[1])
            elif msgType == "SERVERMSG":
                self.txt.insert(tk.END, msgParsed[1])