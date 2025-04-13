# The main show view of the timer app
import tkinter as tk

class MainShowView(tk.Label):
    def __init__(self, context, controller):
        super().__init__()
        self.context = context
        self.controller = controller