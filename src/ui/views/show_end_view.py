# The UI frame for when the show is ended

import tkinter as tk

class ShowEndView(tk.Frame):
    def __init__(self, context, controller):
        super().__init__()
        self.context = context
        self.controller = controller