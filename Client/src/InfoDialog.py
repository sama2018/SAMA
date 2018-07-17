import json
from tkinter import Toplevel, Label, Entry, StringVar, OptionMenu, Button, Text


class InfoDialog(Toplevel):

    def __init__(self):

        # Call constructor
        super(InfoDialog, self).__init__()

        self.title = "Server Information"

        self.on_create_dialog = None

    def create_dialog(self, on_create_dialog_callback):

        # Create server user number info
        self.si_users_label = Label(self, text="users connected")
        self.si_users_container = Text(self, width=40)

        self.si_users_label.grid(row=0, column=0, sticky="w")
        self.si_users_container.grid(row=1, column=0)

        server_info = on_create_dialog_callback()

        # Iterate over connected users
        for user in server_info["user_figure"]:
            self.si_users_container.insert("end", user+"\n")

        print(server_info)













