from tkinter import *
from socket import *
import json
import sys
from Client.src import ClientConnection




class ConnectionDialog:

    def __init__(self, parent):
        self.top = Toplevel(parent)


        global username_holder
        username_holder = StringVar()

        global word_holder
        word_holder = StringVar()

        welcomeMessage = Label(self.top, text="Please provide a USERNAME and select a FIGURE to be drawn.\n"
                                              "You can  enter also the figure by number \n\n"
                                              " 1-CIRCLE  2-TRIAGLE  3-RECTANGLE  4-SQUARE \n ")

        # entry for username with placeholder

        # user_Placeholder = "username"
        entry_username = Entry(self.top, textvariable=username_holder)
        # entry_username.insert(0, user_Placeholder)

        # entry with word selected and placeholder

        # word_Placeholder = "geometric figure"
        entry_GeoFig = Entry(self.top, textvariable=word_holder)
        # entry_GeoFig.insert(0, word_Placeholder)

        connect_Button = Button(self.top, text="Send", command=self.dataHandler)

        # Placing objects in the grid
        welcomeMessage.grid(row=0, column=1)
        entry_username.grid(row=1, column=1)
        entry_GeoFig.grid(row=2, column=1)

        connect_Button.grid(row=4, column=1)

    def ok(self):
        print("Your Username is", self.e.get())
        self.top.destroy()

    def body(self):
        pass
        # Label(self.top, text="Please provide us a username:").grid(row=0, column=0, sticky="w")

        # this function handles the data entred by users

    def dataHandler(self):

        user = username_holder.get()
        wordSelected = word_holder.get()
        #cc = ClientConnection.ClientConnection()

        isUsernameValid = self.user_validation(user)#cc.user_validation(user)
        isWordSelectedValid = self.word_validation(wordSelected) #cc.word_validation(wordSelected)

        if isUsernameValid == True and isWordSelectedValid == True:

            print("ok: " + user + ": "+ wordSelected)

            sentence = user + " " + wordSelected + "\n"
            #cc.connect(sentence)  # call connect
            user_Error = Label(self.top, text=" ", fg="white")
            user_Error.grid(row=6, column=1)

        else:
            # show errors
            print("wrong username entered")
            user_Error = Label(self.top, text="USERNAME OR FIGURE SELECTED WAS INVALID", fg="red")
            user_Error.grid(row=6, column=1)



    @staticmethod
    def build_json_reply(action, payload):
        return json.dumps({"action": action, "payload": payload})

    def mytest(self):
        #if username and fig geo are OK:
        sentence = self.e.get()
        #figGeo = fig.get()
        print(sentence)

        self.clientSocket.sendall(self.build_json_reply("set_username", {"username":sentence}).encode("utf-8"))
        modifiedSentence = self.clientSocket.recv(1024).decode("utf-8")

        print("reply from server: "+ modifiedSentence)



        #self.ClientConnection.connect(sentence)
        self.ok()

    def getUsername(self):
        return self.username

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



        #ClientConnection.connect(sentence)
        #show errors mesagges
        #NOT ALLOWED connection from this client




