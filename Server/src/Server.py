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



def build_json_reply(action, payload):
    return json.dumps({"action": action, "payload": payload})

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
            username = (jdata["payload"]["from"]).upper()
            message = jdata["payload"]["message"]
            print(username)
            print(clients)

            if username in clients:
                print("found username")
                for user in clients:
                    clients[user].sendall(build_json_reply("broadcast_event", {"message":message, "from":username}).encode("utf-8"))

        # code starts here to send the drawings

        elif jdata["action"] == "drawing":
            coordinate1 = jdata["payload"]["coordinate1"]
            coordinate2 = jdata["payload"]["coordinate2"]
            coor1 = str(coordinate1)
            coor2 = str(coordinate2)
            print("receive coords: " + "x: " + coor1 + " y:  " + coor2)


            #for user in clients:
            #clients[user].sendall( build_json_reply("broadcast_event", {"coordinate1": coordinate1, "coordinate2": coordinate2}).encode("utf-8"))
                #print("receive coords")

    conn.close()


""" Enter main loop to accept new clients"""
while 1:
    connectionSocket, addr = serverSocket.accept()
    print("Connected with " + addr[0] + ":" + str(addr[1]))
    start_new_thread(clientT, (connectionSocket,))


serverSocket.close()

