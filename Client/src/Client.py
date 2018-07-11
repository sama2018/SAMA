from Client.src import UI
import socket
from threading import Thread
import json
import sys

class Client(UI):

    SERVER_NAME = "localhost"

    SERVER_PORT = 10000

    def __init__(self):

        # Call parent class constructor
        super(Client, self).__init__()

        self.socket = None

        # Connect to server
        self.connect()

        # Draw UI elements



    @staticmethod
    def build_json_reply(action, payload):
        return json.dumps({"action":action,"payload":payload})

    def connect(self):

        try:
            # Create socket and connect
            self.socket = socket.socket(socket.SOCK_STREAM, socket.SOCK_STREAM)
            self.clientSocket.connect((Client.SERVER_NAME, Client.SERVER_PORT))

            # Create and start new thread to handle server input
            t = Thread(target=self.handle_server_input)
            t.start()

        except socket.error as Error:
            sys.stderr.write("ERROR(1): Unable to connect server - {0}\n".format(Error.strerror))

    def handle_server_input(self):
        pass













