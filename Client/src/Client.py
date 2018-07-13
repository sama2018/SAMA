import socket
from threading import Thread
import json
import sys
from Client.src import UI

class Client:

    SERVER_HOST = 'localhost'

    SERVER_PORT = 10001

    RBUF = 2049

    def __init__(self):

        self.csocket = None

        self.player_db = None

        self.local_user = None


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

            # Receive server reply
            return data

    def handle_server_input(self):

        # Begin main loop
        while True:

            # Receive data from server
            data = json.loads(self.csocket.recv(Client.RBUF).decode("utf-8"))

            # Determine what to do
            if data["action"] == "register_user":
                if data["outcome"] == True:
                    self.player_db = data["payload"]["players"]
            elif data["action"] == "broadcast_drawing":
                pass


    def broadcast_drawing(self, x, y):
        self.csocket.sendall(self.build_json_reply("broadcast_drawing", {"from":self.local_user["username"], "x":x,"y":y, "players":self.player_db}).encode("utf-8"))


















