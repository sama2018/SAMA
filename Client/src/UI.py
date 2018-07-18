from time import sleep
from tkinter import *

class UI:

    wWidth = 1024
    wHeight = 720

    lWidth = 200
    lHeight = 200

    crfWidth = 200
    crfHeight = 420

    def __init__(self):

        # Resolve root element
        self.root = Tk()

        # Canvas db
        self.canvas_db = []

        # Canvas user
        self.canvas_user = {}

        # Previous canvas event
        self.pcanvas_event = None

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
        self.canvasLocal = Frame(self.root, width=200, height=320, bd=1, relief=SUNKEN)

        # Create Chat
        self.chat = Frame(self.root, width=UI.lWidth, height=UI.crfHeight, bd=1, relief=SUNKEN)
        self.chatWindow = Text(self.chat, width=15)

        # Create send image frame
        #self.send_image_frame = Frame(self.root, width=200, height=40, bd=1, relief=SUNKEN)

        # Create option menu that will contain all users which can be sent the drawing
        #self.user_list_dd_value = StringVar(self.send_image_frame)
        #self.user_list_dd_value.set("select user ...")
        #self.user_list_dd_values = ['loading users ...']
        #self.user_list_dropdown = OptionMenu(self.send_image_frame, self.user_list_dd_value, *self.user_list_dd_values)

        # Create send image button
        #self.sendImageButton = Button(self.send_image_frame, text="Send Image")


    def drawLobby(self):

        self.usernameLabel.grid(row=0, column=0, sticky="nsew")
        self.lobby.grid(row=1, column=0, sticky="nsew")
        self.lobby.grid_columnconfigure(1, weight=1)
        self.lobby.grid_rowconfigure(1, weight=1)

    def drawCanvas(self):

        self.canvasRemote.grid(row=0, column=1, sticky="new")
        self.canvasLocal.grid(row=0, column=1, sticky="ews")

        # Create canvas for user1,2 and 3
        self.rc1 = Canvas(self.canvasRemote, width=300, height=320, bd=1, relief=SUNKEN)
        self.rc2 = Canvas(self.canvasRemote, width=300, height=320, bd=1, relief=SUNKEN)
        self.rc3 = Canvas(self.canvasLocal, width=200, height=280, bd=1, relief=SUNKEN)

        # Position canvases
        self.rc1.pack(anchor=W, fill=Y, expand=False, side=LEFT)
        self.rc2.pack(anchor=E, fill=Y, expand=False, side=RIGHT)
        self.rc3.pack(anchor=CENTER, fill=BOTH, expand=True)

        # Put remote canvases in canvas db
        self.canvas_user[self.rc1] = None
        self.canvas_user[self.rc2] = None

        self.canvas_db.append(self.rc1)
        self.canvas_db.append(self.rc2)

        # Attach motion event to local canvas
        self.rc3.bind("<Button-1>", self.event_start_drawing)
        self.rc3.bind("<ButtonRelease-1>", self.event_stop_drawing)

        # Position send image frame
        #self.send_image_frame.grid(row=1, column=1, sticky="ews")

        # Position send image button and send image user list
        #self.user_list_dropdown.pack(anchor=W, fill=Y, expand=False, side=LEFT)
        #self.sendImageButton.pack(anchor=W, fill=Y, expand=False, side=LEFT)


    def drawChat(self, on_chat_send_callback):

        self.chat.grid(row=0, column=2, sticky="nsew")
        self.chat.grid_columnconfigure(0, weight=1)
        self.chat.grid_rowconfigure(0, weight=1)

        self.chatWindow.grid(row=0, column=0, sticky="nsew")
        self.chatWindow.grid_columnconfigure(0, weight=1)
        self.chatWindow.grid_rowconfigure(0, weight=1)

        self.chatInput=Entry(self.chat, width=20)
        chatButton = Button(self.chat, text="Send", command=on_chat_send_callback)
        chatButton.grid(row=0, column=1, sticky="sew")
        self.chatInput.grid(row=0, column=0, sticky="sew")

    def exitOption(self):
            exit()

    def attachMainMenu(self, start_callback, server_info_callback):

        self.mainMenu = Menu(self.root)
        self.mainSubMenu = Menu(self.mainMenu)
        self.root.config(menu=self.mainMenu)

        self.mainSubMenu.add_command(label="Start", command=start_callback)
        self.mainSubMenu.add_command(label="Server Info", command=server_info_callback)
        self.mainSubMenu.add_command(label="Exit", command=self.exitOption)
        self.mainMenu.add_cascade(label="Network", menu=self.mainSubMenu)

    def ui_init(self, on_chat_send_callback, on_close_callback):
        self.drawCanvas()
        self.drawLobby()
        self.drawChat(on_chat_send_callback)
        self.root.protocol("WM_DELETE_WINDOW", on_close_callback)
        self.root.mainloop()

    def event_start_drawing(self, event):
        self.pcanvas_event = event

    def event_stop_drawing(self, event):
        if self.player_db is None:
            print("cant paint no users are connected\n")
        else:
            self.rc3.create_line(self.pcanvas_event.x, self.pcanvas_event.y,  self.rc3.canvasx(event.x), self.rc3.canvasy(event.y))
            sleep(0.3)
            self.broadcast_drawing(self.pcanvas_event.x, self.pcanvas_event.y, event.x, event.y)




















