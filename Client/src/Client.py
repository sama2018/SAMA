from Client.src import UI
from tkinter import simpledialog
from Client.src import ConnectionDialog
import re
from socket import *
from Client.src import ClientConnection
import select
import sys
import json

class Client:

    def __init__(self):

        self.clientSocket = None

        self.ui = UI.UI(self)

        self.ui.drawLobby()
        self.ui.drawCanvas()
        self.ui.drawChat()
        self.ui.attachMainMenu()

        # Connect to server
        self.connect()

        # Pass socket to ui so we can do ui things
        self.ui.setClientSocket(self.clientSocket)

        # Start interface
        self.ui.root.mainloop()




    def connect(self):

        serverName = "localhost"
        serverPort = 10000

        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((serverName, serverPort))

    @staticmethod
    def build_json_reply(action, payload):
        return json.dumps({"action":action,"payload":payload})

    def chatSend(self):
        text = self.ui.chatInput.get()

        self.clientSocket.sendall(self.build_json_reply("chat_message", {"message":text}).encode("utf-8"))

        #receiveing messages from server

        self.ui.chatWindow.insert("end","May>"+text+"\n")




    def validation(self, username): #add regex to this .Also may go to another file
       userValid = False

       if  re.match(r'(\w+\S+)', username, re.M ) :
          userValid = True

       return userValid











