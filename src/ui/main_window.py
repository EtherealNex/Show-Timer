# The main UI that the app refferances off

import tkinter as tk

class MainWindow(tk.Tk):
    def __init__(self, context):
        super().__init__()
        self.context = context
        self.title("Show Timer")
        self.geometry("800x500")
        self._current_view = None

    # This code will handle UI changing
    def _set_view(self, view: tk.Frame):
        if self._current_view:
            for widget in self._current_view.winfo_children():
                widget.destroy()
            self._current_view.destroy()
        
        self._current_view = view
        self._current_view.pack(fill='both', expand=True)
        self.update_idletasks()