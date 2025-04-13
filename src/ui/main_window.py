# The main UI that the app refferances off

import tkinter as tk

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Show Timer")
        self.geometry("800x600")
        self._current_view = None

    def set_view(self, view: tk.Frame):
        if self._current_view:
            self._current_view.destroy()
        
        self._current_view = view
        self._current_view.pack(fill='both', expand=True)