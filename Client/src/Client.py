from threading import Thread
from tkinter import *

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

    cordy1, cordy2 = None, None

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

    def handle_server_input(self, event=None):

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

            if jdata["action"] == "broadcast_event1":
                # Get payload data
                cordy1 = jdata["payload"]["coordinate1"]
                cordy2 = jdata["payload"]["coordinate2"]

                self.ui.rc1.create_line(0, 0, cordy1,cordy2, fill="red", width=4, smooth=TRUE)
                self.ui.rc2.create_line(0, 0, cordy1, cordy2, fill="green", width=4, smooth=TRUE)

                #self.ui.rc1.bind("<B1-Motion>", lambda event : self.receiveFig(cordy1, cordy2,event))




    def receiveFig (self, posX, posY, event = None):

        self.draw_received_figure(posX, posY , event )

    #FIXME !!!!
    def draw_received_figure(self, posX, posY,  obj):

        if posX is not None and posY is not None:

            obj.widget.create_line(posX , posY, obj.x, obj.y, fill="red", width=4, smooth=TRUE)

        posX = obj.x
        posY = obj.y

    def send_drawing_coordinates(self, x, y, username, figure):

        self.clientSocket.sendall(self.build_json_reply("drawing", {"username":username, "figure":figure,"coordinate1": x, "coordinate2": y}).encode("utf-8"))
        data = self.clientSocket.recv(2048).decode("utf-8")
        print(data)



    @staticmethod
    def build_json_reply(action, payload):
        return json.dumps({"action":action,"payload":payload})

    def chatSend(self):

        print("chat send")

        text = self.ui.chatInput.get()

        self.clientSocket.sendall(self.build_json_reply("chat_message", {"from":self.ui.cDialog.getUsername(),"message":text}).encode("utf-8"))















