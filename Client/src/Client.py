import socket
from threading import Thread, Lock
import json
import sys
from time import sleep
from tkinter import END

from Client.src import UI, UserDialog, InfoDialog


class Client(UI.UI):

    SERVER_HOST = 'localhost'

    SERVER_PORT = 10001

    UDP_SERVER_HOST = 'localhost'

    UDP_SERVER_PORT = 10002

    RBUF = 2049

    def __init__(self):

        # Call parent class constructor
        super(Client, self).__init__()

        # TCP Socket (connection to TCP server)
        self.csocket = None

        # UDP Socket (connection to UDP Server)
        self.ucsocket = None

        # Local list of users drawing the same figure
        self.player_db = None

        # Contains the registered user (you)
        self.local_user = None

        # Allows for access of data
        self.mutex = Lock()


    @staticmethod
    def build_json_reply(action, payload):
        return json.dumps({"action":action,"payload":payload})

    def connect(self):
        """ Connect to TCP server"""

        try:
            # Create socket and connect
            self.csocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.csocket.connect((Client.SERVER_HOST, Client.SERVER_PORT))

            # Create and start new thread to handle server input
            t = Thread(target=self.handle_server_input)
            t.start()

        except socket.error as Error:
            sys.stderr.write("ERROR(1): Unable to connect server - {0}\n".format(Error.strerror))

    def register_user(self, values):
        """ Register user with server"""

        if self.csocket is not None:

            # Ask the server to register user
            self.csocket.sendall(self.build_json_reply("register_user", values).encode("utf-8"))

            # Receive server reply
            data = json.loads(self.csocket.recv(Client.RBUF).decode("utf-8"))

            # If reply was a success then save the list of users for the figure
            if data["outcome"] == True:
                # Set local user
                self.local_user = values

                # Update player db
                self.player_db = data["payload"]["players"]

                # Iterate over player db to assign them to remote canvases
                pcount = 0
                for player in self.player_db:
                    if player != self.local_user["username"]:
                            self.canvas_user[self.canvas_db[pcount]] = player
                    pcount += 1

            # Receive server reply
            return data

    def handle_server_input(self):

        # Begin main loop
        while True:

            if not self.csocket:
                return False

            # Receive data from server
            self.mutex.acquire()
            try:
                raw = self.csocket.recv(Client.RBUF).decode("utf-8")
                if raw:
                    data = json.loads(raw)
                else:
                    continue
            finally:
                self.mutex.release()

            # Determine what to do
            if data["action"] == "register_user":
                if data["outcome"] == True:
                    self.player_db = data["payload"]["players"]

                    # Re-assign the canvases after we obtain the new list of players
                    pcount = 0
                    for player in self.player_db:
                        if player != self.local_user["username"]:
                            self.canvas_user[self.canvas_db[pcount]] = player
                            pcount += 1

            elif data["action"] == "broadcast_drawing" and data["outcome"] == True:
                frm = data["payload"]["from"]
                to = data["payload"]["to"]
                x = data["payload"]["x"]
                x_root = data["payload"]["x_root"]
                y = data["payload"]["y"]
                y_root = data["payload"]["y_root"]

                # Look for frm in canvas_user
                for canvas in self.canvas_user:
                    if self.canvas_user[canvas] == frm:
                        canvas.create_line(canvas.canvasx(x_root), canvas.canvasy(y_root), canvas.canvasx(x), canvas.canvasy(y), fill="blue")

            elif data["action"] == "chat_broadcast" and data["outcome"] == True:
                frm = data["payload"]["from"]
                message = data["payload"]["message"]

                # Insert new message into chat window
                self.chatWindow.insert("end", frm+"> "+message+"\n")

    def broadcast_chat_message(self, message):
        if self.csocket is None or self.local_user is None:
            self.chatWindow.insert("end", "ERROR: Please set a username and a figure\n")
            return False
        else:
            self.csocket.sendall(self.build_json_reply("chat_broadcast", {"from":self.local_user["username"], "message":message}).encode("utf-8"))
            self.chatInput.delete(0, 'end')
            return True

    def broadcast_drawing(self, x, y, x_root, y_root):
        self.csocket.sendall(self.build_json_reply("broadcast_drawing", {"from":self.local_user["username"], "x":x,"y":y, "x_root":x_root, "y_root":y_root, "players":self.player_db}).encode("utf-8"))

    def get_info(self):

        # Create tuple for sending data
        to = (Client.UDP_SERVER_HOST, Client.UDP_SERVER_PORT)

        # Create udp socket
        self.ucsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Send packet
        self.ucsocket.sendto(self.build_json_reply("server_info", {}).encode("utf-8"), to)

        # Receive reply
        data, addr = self.ucsocket.recvfrom(Client.RBUF)

        # Encode reply into json
        jdata = json.loads(data.decode("utf-8"))

        # Outcome
        if jdata["outcome"] == True:
            return jdata["payload"]

    def user_dialog(self):

        # Create user dialog
        self.userDialog = UserDialog.UserDialog()

        # Start dialog
        self.userDialog.create_dialog(self.register_user)

    def info_dialog(self):

        # Create info dialog
        self.infoDialog = InfoDialog.InfoDialog()

        # Create dialog
        self.infoDialog.create_dialog(self.get_info)

    def on_window_close(self):

        # Send disconnect event
        if self.csocket:
            #self.csocket.sendall(self.build_json_reply("disconnect", {"from":self.local_user["username"]}).encode("utf-8"))
            self.csocket.close()

        self.root.destroy()

    def start(self):

        # Connect to server
        self.connect()

        # Attach main menu
        self.attachMainMenu(lambda : self.user_dialog(), lambda : self.info_dialog())

        # start ui
        self.ui_init(lambda : self.broadcast_chat_message(self.chatInput.get()), lambda : self.on_window_close())




















