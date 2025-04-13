# The pre show view that is displayed when the app is launched
import tkinter as tk

class PreShowView(tk.Frame):
    def __init__(self, context, controller):
        super().__init__()
        self.context = context
        self.controller = controller

        """ -- CALL FRAME -- """

        self.call_frame = tk.Frame(self)
        self.call_frame.pack(fill='x')

        show_call_button = tk.Button(self.call_frame, text='Next Show Call',
                                      font=("Helvetica", 14), width=15,
                                      #command =
                                      relief='solid', border=2)
        show_call_button.pack(side='top', pady=10)

        next_call_label = tk.Label(self.call_frame, text=f"Next Call: N/A", fg="lightgrey", font=("Helvetica", 14)) # Logic for displaying next call
        next_call_label.pack()

        current_call_label = tk.Label(self.call_frame, text="Current Call:", font=("Helvetica", 16))
        current_call_label.pack(pady=2)

        current_call_timer_lable = tk.Label(self.call_frame, text="", font=("Helvetica",0), fg='lightgrey')
        current_call_timer_lable.pack(pady=0)


        """ -- CENTER LABEL AND GLOBAL TIMER -- """

        self.center_frame = tk.Frame(self)
        self.center_frame.place(relx=0.5,rely=0.5, anchor='center')

        title_label = tk.Label(self.center_frame, text="Show Timer", font=("Helvetica", 48))
        title_label.pack(pady=(0,5))

        local_timer_label = tk.Label(self.center_frame, text="00:00:00", font=("Helvetica", 42), fg="lightgrey")
        local_timer_label.pack()

        """ -- BOTTOM BUTTONS -- """

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side='bottom', pady=10)

        start_frame = tk.Frame(self)
        start_frame.pack(side='bottom', pady=0)

        start_show_button = tk.Button(start_frame, text="Start Show", font=("Helvetica", 14), width=20)
        start_show_button.pack(anchor='center')

        view_show_stats = tk.Button(self.button_frame, text='Show Stats', font=("Helvetica", 14), width=10, command=controller.open_stats_window)
        view_show_stats.grid(column=0, row=0, padx=5)

        settings_window_button = tk.Button(self.button_frame, text="Settings", font=("Helvetica", 14), width=10, command=controller.open_setting_window)
        settings_window_button.grid(column=1, row=0, padx=5)