# The large timer widget window

import tkinter as tk

class TimerWindow(tk.Tk):
    def __init__(self, context, controller):
        super().__init__()
        self.context = context
        self.controller = controller

        self.title("Show Timer Clock")
        self.geometry("1000x400")
        self.resizable(True, True)

        # Bind the closing button.
        self.bind("<Destroy>", self.controller.on_timer_window_destroy)

        """ -- UI -- """

        header_label = tk.Label(self, text='Show Timer', font=("Helvetica", 48), fg='lightgrey')
        header_label.pack(pady=5)

        center_frame = tk.Frame(self)
        center_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.local_timer_label = tk.Label(center_frame,
                                            text="00:00:00",
                                            font=("Helvetica", 108, "bold")
                                        )
        
        self.local_timer_label.pack()

