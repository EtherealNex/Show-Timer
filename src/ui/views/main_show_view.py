# The main show view of the timer app
import tkinter as tk

class MainShowView(tk.Frame):
    def __init__(self, context, controller):
        super().__init__()
        self.context = context
        self.controller = controller

        """ -- STOP SHOW -- """
        stop_show_button = tk.Button(self, text="Stop Show", font=("Helvetica", 14), width=15,
                                     # command
                                     fg='red',
                                     relief='solid', borderwidth=2,
                                     highlightthickness=0)
        stop_show_button.pack(side='top', pady=10)

        """ -- CENTER FRAME TIMERS -- """

        self.center_frame = tk.Frame(self)
        self.center_frame.pack(expand=True)

        show_stopped_timer_label = tk.Label(self.center_frame, font=("Helvetica", 36, "bold"), text="TE:MP:ST:OP", fg="#D32F2F")
        show_stopped_timer_label.pack(side='top', pady=5)

        main_show_timer_label = tk.Label(self.center_frame, font=("Helvetica", 48), text='00:00:00:00')
        main_show_timer_label.pack(pady=(0, 5))

        self.local_timer_label = tk.Label(self.center_frame, text="00:00:00", font=("Helvetica", 42), fg="lightgrey")
        self.local_timer_label.pack()

        """ -- NEXT MENU BUTTON -- """
        # This will need some code to change the text depending on what comes next, either interval or end of show
        # A backend function will have to change the label on this button depedning on what is next either 'act down' or 'end show'

        next_segment_button = tk.Button(self, text="Next Seg", width=15, borderwidth=2)
        next_segment_button.pack(side='bottom', pady=20)

        
    # back end testing // RELOOK AT and fix code to be cleaner
    def reset_state(self):
        # Clean up widgets that wont be catched
        for widget in self.winfo_children():
            widget.destroy()
        self.__init__(context=self.context, controller=self.controller)