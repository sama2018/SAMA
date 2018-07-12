from tkinter import *
import sys
from Client.src import ConnectionDialog
import json
from socket import *
from Client.src import Client


class UI:

    wWidth = 1024
    wHeight = 720

    lWidth = 100
    lHeight = 200

    crfWidth = 200
    crfHeight = 420

    style = "freeStyle"
    pos = "down"

    x_pos, y_pos = None, None


    def __init__(self, client):

        #self.cd = ConnectionDialog.ConnectionDialog(self) #getting object from ConnectionDialog



        #self.clientSocket = None
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect(('localhost',10000))

        self.client = client

        # Resolve root element
        self.root = Tk()

        # Set window geometry
        self.root.geometry(str(UI.wWidth) +"x"+ str(UI.wHeight))

        # Set it so it is resizable
        self.root.resizable(True, True)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        # Create lobby frame
        self.lobby = Frame(self.root, width=UI.lWidth, height=UI.lHeight, bd=1, relief=SUNKEN)
        self.usernameLabel = Label(self.lobby, text="Placeholder")

        # Create canvases
        self.canvasRemote = Frame(self.root, width=UI.crfWidth, height=UI.crfHeight, bd=1, relief=SUNKEN)
        self.rc1 = Canvas(self.canvasRemote, width=213, height=320, bd=1, relief=SUNKEN)
        self.rc2 = Canvas(self.canvasRemote, width=213, height=320, bd=1, relief=SUNKEN)

        self.canvasLocal = Frame(self.root, width=200, height=320, bd=1, relief=SUNKEN)

        # Create Chat
        self.chat = Frame(self.root, width=UI.lWidth, height=UI.crfHeight, bd=1, relief=SUNKEN)
        self.chatWindow = Text(self.chat)

        self.cDialog = None



    def setClientSocket(self, clientSocket):
        self.clientSocket = clientSocket

    def drawLobby(self):

        self.usernameLabel.grid(row=0, column=0, sticky="nsew")
        self.lobby.grid(row=1, column=0, sticky="nsew")
        self.lobby.grid_columnconfigure(1, weight=1)
        self.lobby.grid_rowconfigure(1, weight=1)

    def drawCanvas(self):

        self.canvasRemote.grid(row=0, column=1, sticky="new")
        self.canvasLocal.grid(row=0, column=1, sticky="ews")

        # Create canvas for user1,2 and 3
        self.me = Canvas(self.canvasLocal, width=380, height=320, bd=1, relief=SUNKEN)

        self.rc1.grid(row=0, column=0, sticky="e")
        self.rc2.grid(row=0, column=1, sticky="w")

        #self.rc1.bind("<B1-Motion>", lambda event : self.mydraw_Action(event))


        # Create user canvas
        self.me.grid(row=0, column=0, sticky="e")

    #------------------------------------------ NEW CODE FROM HERE  -----------------------------------------------
        #me.bind("<B1-Motion>", self.draw_Action) #we can specify diffenrent events here
        self.me.bind("<Button-1>", self.draw_Action)
       


    def mydraw_Action(self, event):
            cl = Client.Client()


            if cl.cordy1 is not None and cl.cordy2 is not None:

                    self.draw_figure_selected(event)


            cl.cordy1 = event.x
            cl.cordy2 = event.y




    # see if we can implement interface features to allow users to select colors and width to draw
    def draw_Action(self, event=None):

        if self.style == "freeStyle":

            if self.pos == "down":


                if self.x_pos is not None and self.y_pos is not None:

                    self.draw_figure_selected(event)


                self.x_pos = event.x
                self.y_pos = event.y

                self.client.send_drawing_coordinates(self.x_pos, self.y_pos, self.cDialog.getUsername(), self.cDialog.getFigure() )





    """this function is going to create the figures
       From here we can manage the different inputs and enable users to draw according to that"""

    def draw_figure_selected(self, obj):

            #if self.cd.getFigure() == 'triangle':
            obj.widget.create_line(self.x_pos, self.y_pos, obj.x, obj.y, fill="blue", width=4, smooth=TRUE)


            #else :




    #we need thisfuction again here to notify the server of the action to take
    @staticmethod
    def build_json_reply(action, payload):
        return json.dumps({"action": action, "payload": payload})

    #------------------------------------------------ UNTIL HERE ---------------------------------------------------


    def mayClick(self):

        self.client.chatSend()



    def drawChat(self):

        self.chat.grid(row=0, column=2, sticky="nsew")
        self.chat.grid_columnconfigure(0, weight=1)
        self.chat.grid_rowconfigure(0, weight=1)

        self.chatWindow.grid(row=0, column=0, sticky="nsew")
        self.chatWindow.grid_columnconfigure(0, weight=1)
        self.chatWindow.grid_rowconfigure(0, weight=1)

        self.chatInput=Entry(self.chat, width=20)
        chatButton = Button(self.chat, text="Send", command =self.mayClick)
        chatButton.grid(row=0, column=1, sticky="sew")
        self.chatInput.grid(row=0, column=0, sticky="sew")


    def callback(self):
        #self.label(text="Please provide us a username")
        self.cDialog = ConnectionDialog.ConnectionDialog(self.root, self.clientSocket)
        #self.cDialog.body()


    def exitOption(self):
            exit()

    def attachMainMenu(self):

        self.mainMenu = Menu(self.root)
        self.mainSubMenu = Menu(self.mainMenu)
        self.root.config(menu=self.mainMenu)
        self.mainSubMenu.add_command(label="Start", command=self.callback)
        self.mainSubMenu.add_command(label="Exit", command=self.exitOption)
        self.mainMenu.add_cascade(label="Network", menu=self.mainSubMenu)




















