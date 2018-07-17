import socket
import threading
import json
import sys

class Server:

    HOST = "localhost"
    PORT = 10001
    RBUF = 2049
    UDP_HOST = "localhost"
    UDP_PORT = 10002
    VERSION = "1.0.0"
    AUTHORS = ["Mayrelis Morejon", "Samira Tellez"]

    def __init__(self):

        # Server socket
        self.server_socket = None

        # UDP server socket
        self.udp_server_socket = None

        # Server backlog
        self.backlog = 10

        # Keep a dictionary with user => socket
        self.user_db = {}

        # Keep a dictionary with user => figure
        self.figure_db = {}

    @staticmethod
    def build_json_reply(action, outcome, payload):
        return json.dumps({"action":action, "outcome":outcome, "payload":payload})

    def start(self):

        # Resolve TCP socket
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as Error:
            sys.stderr.write("ERROR: unable to resolve tcp socket - {0}\n".format(Error.strerror))
            exit(-1)

        # Set socket as re-usable
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind socket
        try:
            self.server_socket.bind((Server.HOST, Server.PORT))
        except socket.error as Error:
            sys.stderr.write("ERROR: unable to bind socket - {0}\n".format(Error.strerror))
            exit(-1)

        # Start to listen
        self.server_socket.listen(self.backlog)

        # Enter main accept loop
        while True:
            sys.stdout.write("TCP> waiting for connection\n")

            client_socket, client_addr = self.server_socket.accept()

            sys.stdout.write("TCP>> incoming connection from {0}:{1}\n".format(client_addr[0], client_addr[1]))

            # Create new thread to handle connection
            new_client_thread = threading.Thread(target=self.new_client, args=(client_socket, client_addr,))
            new_client_thread.start()

    def udp_start(self):

        # Resolve UDP socket
        try:
            self.udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error as Error:
            sys.stderr.write("ERROR: unable to resolve udp socket - {0}\n".format(Error.strerror))
            return False

        # Bind socket
        try:
            self.udp_server_socket.bind((Server.UDP_HOST, Server.UDP_PORT))
        except socket.error as Error:
            sys.stderr.write("ERROR: unable to bind udp socket - {0}\n".format(Error.strerror))
            exit(-1)

        # Enter main loop
        while True:
            print("UDP> waiting for connection\n")
            data, client_addr = self.udp_server_socket.recvfrom(Server.RBUF)
            sys.stdout.write("UDP>> incoming message from {0}:{1}\n".format(client_addr[0], client_addr[1]))

            # Create new thread to handle udp data
            new_udp_client_thread = threading.Thread(target=self.new_udp_client, args=(data.decode("utf-8"), client_addr,))
            new_udp_client_thread.start()

    def new_client(self, csocket, caddr):

        # Enter infinite recv loop
        while True:

            if not csocket:
                return False

            rdata = json.loads(csocket.recv(Server.RBUF).decode("utf-8"))

            if not rdata:
                return False

            if rdata["action"] == "register_user":
                self.a_register_user(rdata["payload"], csocket)
            elif rdata["action"] == "broadcast_drawing":
                self.a_broadcast_drawing(rdata["payload"])
            elif rdata["action"] == "chat_broadcast":
                self.a_chat_broadcast(rdata["payload"])
            elif rdata["action"] == "disconnect":
                self.a_disconnect(rdata["payload"])
            elif rdata["action"] == "get_users":
                self.a_get_users(rdata["payload"], csocket)

    def new_udp_client(self, data, caddr):

        # Convert data into json
        jdata = json.loads(data)

        # Decide what to do
        if jdata["action"] == "server_info":
            self.a_udp_server_info(jdata["payload"], caddr)




    def count_user_figure(self, user, figure):

        count = 0

        for _user in self.figure_db:
            if self.figure_db[_user] == figure:
                count += 1

        return count

    def get_users_for_figure(self, figure):

        # Holds figures
        users = []

        # Iterate over figure
        for user in self.figure_db:
            if self.figure_db[user] == figure and user in self.user_db:
                users.append(user)

        return users

    def update_connected_players_for_figure(self, figure):

        # Iterate over figure db
        for _user in self.figure_db:
            if self.figure_db[_user] == figure:

                # Send that user the list of user for figure
                self.user_db[_user].sendall(self.build_json_reply("register_user", True, {"players":self.get_users_for_figure(figure)}).encode("utf-8"))

    def remove_player_from_server(self, player):
        pass

    def a_register_user(self, data, csocket):

        # Get data values
        username = data["username"]
        figure = data["figure"]

        # Count how many users for a figure
        if self.count_user_figure(username, figure) >= 3:
            csocket.sendall(self.build_json_reply("register_user", False, {"message":"The figure chosen has reached it's limits"}).encode("utf-8"))
            return False

        # Add user to list
        self.user_db[username] = csocket
        self.figure_db[username] = figure

        # Get all users for that figure and send them to the client
        csocket.sendall(self.build_json_reply("register_user", True, {"players":self.get_users_for_figure(figure)}).encode("utf-8"))

        # Update connected players for users
        self.update_connected_players_for_figure(figure)

        return True

    def a_broadcast_drawing(self, data):

        # Iterate over player list
        for player in data["players"]:
            if player != data["from"] and player in self.user_db:
                self.user_db[player].sendall(self.build_json_reply("broadcast_drawing", True, {"from":data["from"], "to":player, "x":data["x"], "y":data["y"], "x_root":data["x_root"], "y_root":data["y_root"]}).encode("utf-8"))

    def a_chat_broadcast(self, data):

        # Iterate over all users and send the message
        for user in self.user_db:
            self.user_db[user].sendall(self.build_json_reply("chat_broadcast", True, {"from":data["from"], "message":data["message"]}).encode("utf-8"))

    def a_disconnect(self, data):
        pass

    def a_udp_server_info(self, data, addr):

        # Holds list of users
        user_list = []

        # Iterate to get just the users
        for user in self.user_db:
            user_list.append(user)

        self.udp_server_socket.sendto(self.build_json_reply("server_info", True, {
            "users":user_list,
            "user_figure": self.figure_db,
            "version":Server.VERSION,
            "authors":Server.AUTHORS
        }).encode("utf-8"), addr)









