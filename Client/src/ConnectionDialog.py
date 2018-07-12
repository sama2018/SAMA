from tkinter import *
from socket import *
import json
import sys
from Client.src import ClientConnection




class ConnectionDialog:

    def __init__(self, parent, socket):

        self.top = Toplevel(parent)
        self.clientSocket = socket
        self.username = None
        self.word = None


        global username_holder
        username_holder = StringVar()

        global word_holder
        word_holder = StringVar()

        welcomeMessage = Label(self.top, text="Please provide a USERNAME and select a FIGURE to be drawn.\n"
                                              "You can  enter also the figure by number \n\n"
                                              " 1-CIRCLE  2-TRIANGLE  3-RECTANGLE  4-SQUARE \n ")

        # entry for username with placeholder


        entry_username = Entry(self.top, textvariable=username_holder)


        entry_GeoFig = Entry(self.top, textvariable=word_holder)


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


     # this function handles the data entered by users

    def dataHandler(self):

        user = username_holder.get()
        self.username = user
        wordSelected = word_holder.get()
        self.word = wordSelected

        isUsernameValid = self.user_validation(user)#cc.user_validation(user)
        isWordSelectedValid = self.word_validation(wordSelected) #cc.word_validation(wordSelected)



        if isUsernameValid == True and isWordSelectedValid == True:

            print("ok: " + user + ": "+ wordSelected)

            wordSelected = wordSelected + "\n"



            self.clientSocket.sendall(self.build_json_reply("set_username", {"username": user, "figure":wordSelected}).encode("utf-8"))
            modifiedSentence = self.clientSocket.recv(1024).decode("utf-8")

            print("reply from server: " + modifiedSentence)
            #try to make dessapear this pop up window when user is authenticated
            self.top.withdraw()

        else:
            # show errors
            print("wrong username entered")
            user_Error = Label(self.top, text="USERNAME OR FIGURE SELECTED WAS INVALID", fg="red")
            user_Error.grid(row=6, column=1)



    @staticmethod
    def build_json_reply(action, payload):
        return json.dumps({"action": action, "payload": payload})

    """def mytest(self):
        #if username and fig geo are OK:
        sentence = self.e.get()
        #figGeo = fig.get()
        print(sentence)

        self.clientSocket.sendall(self.build_json_reply("set_username", {"username":sentence}).encode("utf-8"))
        modifiedSentence = self.clientSocket.recv(1024).decode("utf-8")

        print("reply from server: "+ modifiedSentence



        #self.ClientConnection.connect(sentence)
        self.ok()"""

    def getUsername(self):
        return self.username

    def getFigure(self):
        return self.word


    def user_validation(self, username):  # add regex to this .Also may go to another file
        userValid = False

        if re.match(r'(\w+\S+)', username, re.M):
            userValid = True

        return userValid

    def word_validation(self, word_selected):
        wordValid = False

        # fix this
        word_selected = word_selected.upper()

        # change words to upper Case

        if re.match(r'CIRCLE', word_selected, re.M) or word_selected == '1':
            wordValid = True
        if re.match(r'TRIANGLE', word_selected, re.M) or word_selected == '2':
            wordValid = True
        if re.match(r'RECTANGLE', word_selected, re.M) or word_selected == '3':
            wordValid = True
        if re.match(r'SQUARE', word_selected, re.M) or word_selected == '4':
            wordValid = True

        return wordValid








