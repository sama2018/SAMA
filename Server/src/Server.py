from socket import *
import json
from _thread import *
import sys

#This function takes the data enters by the user and handles it to write into a file
def createDict(sentence) :
    f  =  open('users.txt', 'a')

    f.write(sentence )

    user = sentence.split(" ")[0]
    word = sentence.split(" ")[1]
    message= "Added:\nuser: " + user + "\n" + "word: " + word
    #test
    return message

serverPort = 10000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("localhost", serverPort))
serverSocket.listen(10)

clients = {}
print('The server is ready to receive')


def clientT(conn):

    while True:

        data = conn.recv(1024).decode()
        if not data:
            break;

        # Turn data into json object
        jdata = json.loads(data)
        if jdata["action"] == "set_username":

            capitalizedSentence = jdata["payload"]["username"].upper()
            clients[capitalizedSentence] = conn
            conn.send(capitalizedSentence.encode())

        elif jdata["action"] == "chat_message":




            # Do chat stuff here
            pass




    conn.close()


while 1:
    connectionSocket, addr = serverSocket.accept()
    print("Connected with " + addr[0] + ":" + str(addr[1]))
    start_new_thread(clientT, (connectionSocket,))


serverSocket.close()

