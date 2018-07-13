import socket
from threading import Thread, Lock
import json
import sys
from time import sleep

from Client.src import UI, UserDialog


class Client(UI.UI):

    SERVER_HOST = 'localhost'

    SERVER_PORT = 10001

    RBUF = 2049

    def __init__(self):

        # Call parent class constructor
        super(Client, self).__init__()

        self.csocket = None

        self.player_db = None

        self.local_user = None

        self.mutex = Lock()


    @staticmethod
    def build_json_reply(action, payload):
        return json.dumps({"action":action,"payload":payload})

    def connect(self):

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


                print(self.canvas_user)


            # Receive server reply
            return data

    def handle_server_input(self):

        # Begin main loop
        while True:

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

                    pcount = 0
                    for player in self.player_db:
                        if player != self.local_user["username"]:
                            self.canvas_user[self.canvas_db[pcount]] = player
                        pcount += 1

                    print(self.canvas_user)

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

            sleep(0.5)


    def broadcast_drawing(self, x, y, x_root, y_root):
        self.csocket.sendall(self.build_json_reply("broadcast_drawing", {"from":self.local_user["username"], "x":x,"y":y, "x_root":x_root, "y_root":y_root, "players":self.player_db}).encode("utf-8"))

    def user_dialog(self):

        # Create user dialog
        self.userDialog = UserDialog.UserDialog()

        # Start dialog
        self.userDialog.create_dialog(self.register_user)

    def start(self):

        # Connect to server
        self.connect()

        # Attach main menu
        self.attachMainMenu(lambda : self.user_dialog())

        # start ui
        self.ui_init()




















