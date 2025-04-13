# A popout widget that controls the timers settings
# This settings widget wont be here in the larger app as that will be controlled globaly, however for now this is here
# When this goes it will be replaced by the large_time_widget.py

import tkinter as tk

class SettingsWindow:
    def __init__(self, context, controller):
        self.context = context
        self.controller = controller

        self.root = tk.Tk()
        self.root.geometry("450x450")
        self.root.resizable(False, False)
        self.root.title("Show Timer Settings")

        # When the window is closed, allow it to reopen again
        self.root.bind("<Destroy>", controller.on_settings_destory)

        """ -- UI CODE -- """

        header_label = tk.Label(self.root, text='Settings', font=("Helvetica", 30))
        header_label.pack(anchor='center', pady=10)
