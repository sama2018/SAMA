from Server.src import Server
from threading import Thread

def main():

    # Create server object
    server = Server.Server()

    # Start and start TCP server thread
    tcp_server_thread = Thread(target=server.start)
    tcp_server_thread.start()

    # Create and start UDP server thread
    udp_server_thread = Thread(target=server.udp_start)
    udp_server_thread.start()

if __name__ == "__main__":
    main()