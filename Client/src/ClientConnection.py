from socket import *
import json
import re


class ClientConnection:

    def __init__(self):
        self.clientSocket = None

    def connect(self, sentence):

        serverName = "localhost"
        serverPort = 10000

        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((serverName, serverPort))

        #while True:

        self.clientSocket.sendall(sentence.encode("utf-8"))
        modifiedSentence = self.clientSocket.recv(1024).decode("utf-8")

        print("reply from server: "+ modifiedSentence)

        return modifiedSentence



