from socket import *
import json
from _thread import *
import sys

#This function takes the data enters by the user and handles it to write into a file
def saveUsers(user, word) :
    f  =  open('users.txt', 'a+')

    f.write(user+ ": " + word )


    return user+word

""" Create socket, bind it to localhost and start to listen for incomming connections"""
serverPort = 10000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("localhost", serverPort))
serverSocket.listen(10)

clients = {}
print('The server is ready to receive')


def clientT(conn):

    """ This method handles the new client by identifying which action to take based on the
        data sent by the client.
    """

    while True:

        data = conn.recv(1024).decode()
        if not data:
            break;

        # Turn data into json object
        jdata = json.loads(data)
        if jdata["action"] == "set_username":
            user = jdata["payload"]["username"].upper()
            word = jdata["payload"]["figure"]
            print("Server msg: user: {0} and word {1}".format(user, word))
            saveUsers(user, word)
            clients[user] = conn
            conn.send(user.encode())

        elif jdata["action"] == "chat_message":
            pass


    conn.close()


""" Enter main loop to accept new clients"""
while 1:
    connectionSocket, addr = serverSocket.accept()
    print("Connected with " + addr[0] + ":" + str(addr[1]))
    start_new_thread(clientT, (connectionSocket,))


serverSocket.close()

