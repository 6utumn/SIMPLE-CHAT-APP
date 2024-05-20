import tkinter as tk
from tkinter import END

import socket as sk
import threading as th

import hashlib

TargetIP = "http://0.tcp.jp.ngrok.io"
PORT     = 19492

Server   = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
Server.connect((TargetIP, PORT))

hostname = sk.gethostname()
IPAddr = sk.gethostbyname(hostname)

Name = hashlib.sha512(IPAddr.encode()).hexdigest()

class MainGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.__Nick = Name[0:3]+Name[7:10]

        self.title("S&C")
        self.geometry("500x405")

        self.Chat = tk.Text(self)
        self.Chat.insert(END, "")
        self.Chat.pack()

        self.Entry = tk.Entry(self)
        self.Entry.pack()

        self.Send  = tk.Button(self, text="SEND", command=self.Send)
        self.Send.pack()

        R = th.Thread(target=self.answerGet)
        R.start()

        self.mainloop()

    def Send(self):
        Server.sendall((self.__Nick+": "+self.Entry.get()).encode())

    def answerGet(self):
        while True:
            data = Server.recv(1024)

            self.Chat.insert(END, f"{data.decode()}\n")





app = MainGUI()