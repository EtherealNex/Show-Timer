# Conatins the stats of all shows foung in user data
# When upgraded to larger app, this will only show the stats for the current show the app has loaded
import tkinter as tk

class ShowStats:
    def __init__(self, context, controller):
        self.context = context
        self.controller = controller

        self.root = tk.Tk()
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        self.root.title("Show Stats Viewer")

        # Bind the closing to only allow one window open
        self.root.bind("<Destroy>", controller.on_stats_window_destory)