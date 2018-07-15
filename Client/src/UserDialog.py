import json
from tkinter import Toplevel, Label, Entry, StringVar, OptionMenu, Button


class UserDialog(Toplevel):

    def __init__(self):

        # Call constructor
        super(UserDialog, self).__init__()

        self.title = "User Information"

        self.on_ok = None

    def create_dialog(self, on_ok_callback):

        # Set on ok callback event
        self.on_ok = on_ok_callback

        # Username label and entry
        self.username_label = Label(self, text="Username")
        self.username_entry = Entry(self)

        # Figure to draw label and entry
        self.figure_label = Label(self, text="Choose Figure")
        self.figure_choices = ('circle', 'triangle', 'square', 'rectangle')
        self.figure_chosen = StringVar(self)
        self.figure_dropdown = OptionMenu(self, self.figure_chosen, *self.figure_choices)

        # Error label
        self.error_label = Label(self)

        # Action button
        self.action_button = Button(self, text="Go !", command=self.ok)

        # Position the username elements
        self.username_label.grid(row=0, column=0)
        self.username_entry.grid(row=0, column=1)

        # Position figure
        self.figure_label.grid(row=1, column=0)
        self.figure_dropdown.grid(row=1, column=1)
        self.figure_dropdown.config(width=20)

        # Position error label
        self.error_label.grid(row=2, column=1, sticky="w")

        # Position button
        self.action_button.grid(row=2, column=1, sticky="e")

    def ok(self):

        # Validate
        # TODO

        # Build reply string
        values = json.loads('{"username":"'+self.username_entry.get()+'", "figure":"'+self.figure_chosen.get()+'"}')

        # Return json reply
        ret = self.on_ok(values)

        if ret["outcome"] == False:
            self.error_label.config(text=ret["payload"]["message"])
        else:
            self.destroy()










