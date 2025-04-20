# The interval view of the show timer

import tkinter as tk

class IntervalView(tk.Frame):
    def __init__(self, context, controller):
        super().__init__()
        self.context = context
        self.controller = controller

        begginers_label = tk.Label(self, text='Begginers', font=("Helvetica", 16), fg='lightgrey')
        begginers_label.pack(pady=5)
        
        begginers_time_label = tk.Label(self, text="TE:MP:00", font=("Helvetica", 14), fg='lightgrey')
        begginers_time_label.pack(pady=2)

        self.center_frame = tk.Frame(self)
        self.center_frame.pack(expand=True)

        interval_timer_label = tk.Label(self.center_frame, text="00:00:00", font=("Helvetica", 48))
        interval_timer_label.pack(pady=(0,5))

        self.local_timer_label = tk.Label(self.center_frame, text="00:00:00", font=("Helvetica", 42), fg='lightgrey')
        self.local_timer_label.pack()

        end_interval_button = tk.Button(self, text="End Interval", font=("Helvetica", 14), width=15, command=self.controller.change_to_main_show_view)
        end_interval_button.pack(side='bottom', pady=20)