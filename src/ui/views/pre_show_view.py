# The pre show view that is displayed when the app is launched
import tkinter as tk

class PreShowView(tk.Frame):
    def __init__(self, context, controller):
        super().__init__()
        self.context = context
        self.controller = controller

        tk.Label(self, text='Pre-Show Setup').pack(pady=20)
        tk.Button(self, text='Start Show', command=self.controller.start_show).pack()