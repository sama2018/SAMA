from threading import Thread

from Client.src import UI
from tkinter import simpledialog
from Client.src import ConnectionDialog
import re
from socket import *
from Client.src import ClientConnection
import select
import sys
import json
from _thread import *

class Client:
    """
     This constructor initializes the client socket
     it creates the UI object and calls all methods
     in charge of drawing the ui components. It also connects
     to the server automatically.
        """
    def __init__(self):

        self.clientSocket = None
        #object of the UI
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



        # # Create thread
        t = Thread(target=self.handle_server_input)
        t.start()

    def handle_server_input(self):

        while True:
            print("WE HERE")
            if self.clientSocket is None:
                print("HERE")
                break
            # Receive data from server
            data = self.clientSocket.recv(2048).decode("utf-8")

            # Convert it to json object
            jdata = json.loads(data)
            print(jdata)


            if jdata["action"] == "broadcast_event":

                # Get payload data
                frm = jdata["payload"]["from"]
                msg = jdata["payload"]["message"]

                # Insert the message into window chat
                self.ui.chatWindow.insert("end", frm+"> "+msg+"\n")



    @staticmethod
    def build_json_reply(action, payload):
        return json.dumps({"action":action,"payload":payload})

    def chatSend(self):

        print("chat send")

        text = self.ui.chatInput.get()

        self.clientSocket.sendall(self.build_json_reply("chat_message", {"from":self.ui.cDialog.getUsername(),"message":text}).encode("utf-8"))





    def validation(self, username): #add regex to this .Also may go to another file
        """ This method validates the username """
        userValid = False

        if  re.match(r'(\w+\S+)', username, re.M ):
              userValid = True

        return userValid











