# The main show view of the timer app
import tkinter as tk

class MainShowView(tk.Frame):
    def __init__(self, context, controller):
        super().__init__()
        self.context = context
        self.controller = controller

        """ -- STOP SHOW -- """
        self.stop_show_button = tk.Button(self, text="Show Stop", font=("Helvetica", 14), width=15,
                                     command = self.controller.start_show_stop,
                                     fg='red',
                                     relief='solid', borderwidth=2,
                                     highlightthickness=0)
        self.stop_show_button.pack(side='top', pady=10)

        """ -- CENTER FRAME TIMERS -- """

        self.center_frame = tk.Frame(self)
        self.center_frame.pack(expand=True)

        self.show_stopped_timer_label = tk.Label(self.center_frame, font=("Helvetica", 0, "bold"), text="", fg="#D32F2F")
        self.show_stopped_timer_label.pack(side='top', pady=5)

        self.main_show_timer_label = tk.Label(self.center_frame, font=("Helvetica", 48), text='00:00:00:00')
        self.main_show_timer_label.pack(pady=(0, 5))

        self.local_timer_label = tk.Label(self.center_frame, text="00:00:00", font=("Helvetica", 42), fg="lightgrey")
        self.local_timer_label.pack()

        """ -- NEXT MENU BUTTON -- """
        # This will need some code to change the text depending on what comes next, either interval or end of show
        # A backend function will have to change the label on this button depedning on what is next either 'act down' or 'end show'

        self.next_segment_button = tk.Button(self, text="Next Seg", width=15, borderwidth=2)
        self.next_segment_button.pack(side='bottom', pady=20)