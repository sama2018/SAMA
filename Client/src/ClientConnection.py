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



    def user_validation(self, username):  # add regex to this .Also may go to another file
        userValid = False

        if re.match(r'(\w+\S+)', username, re.M):
            userValid = True

        return userValid

    def word_validation(self, word_selected):
        wordValid = False

        if re.match(r'circle', word_selected, re.M) or word_selected == '1':
            wordValid = True
        if re.match(r'triagle', word_selected, re.M) or word_selected == '2':
            wordValid = True
        if re.match(r'rectangle', word_selected, re.M) or word_selected == '3':
            wordValid = True
        if re.match(r'square', word_selected, re.M) or word_selected == '4':
            wordValid = True

        return wordValid
