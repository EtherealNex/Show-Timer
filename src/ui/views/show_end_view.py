# The UI frame for when the show is ended

import tkinter as tk
from tkinter import ttk

class ShowEndView(tk.Frame):
    def __init__(self, context, controller):
        super().__init__()
        self.context = context
        self.controller = controller

        """ -- Header Frame -- """
        header_frame = tk.Frame(self, height=50)
        header_frame.pack(fill="x")
        tk.Label(header_frame, text='Show Insights', font=("Helvetica", 36, "bold")).pack(side='top', pady=(10,0))

        self.show_start_stop_local_time_label = tk.Label(header_frame, text='Start: 00:00:00 | End: 00:00:00',
                                                          font=("Helvetica", 20, 'italic'))
        self.show_start_stop_local_time_label.pack(side='top', pady=5)

        # Divider
        divider = tk.Frame(self, height=1, bg='lightgrey')
        divider.pack(fill='x', padx=20)

        """ -- Show Data -- """
        self.show_data_container = tk.Frame(self)
        self.show_data_container.pack(fill='both', expand=True)

        # Canvas, scrollbar, and insight frame
        self.canvas = tk.Canvas(self.show_data_container)
        self.scrollbar = ttk.Scrollbar(self.show_data_container,
                                      orient='vertical',
                                      command=self.canvas.yview
                                      )
        self.show_data_frame = tk.Frame(self.canvas)

        self.show_data_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas_window = self.canvas.create_window((0,0), window=self.show_data_frame, anchor='nw')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width)
        )

        self.canvas.pack(side='left', fill='both', expand=True)

        if int(self.context.settings_interval_count) > 1: # Only place in a scrollbar if there are more than 1 intervals aka > 2 acts. Otherwise standard formatting will cover it
            self.scrollbar.pack(side='right', fill='y')

        # Divider
        divider = tk.Frame(self, height=1, bg='lightgrey')
        divider.pack(fill='x', padx=20, pady=2)

        # Key info frame
        key_info_frame = tk.Frame(self)
        key_info_frame.pack()
        
        self.total_show_stop_time_label = tk.Label(key_info_frame, text=f'Show Stopped Time: N/A', font=("Helvetica", 20))
        self.total_show_stop_time_label.pack(anchor='center')

        self.total_stage_time_label = tk.Label(key_info_frame, text=f'Total Stage Time: N/A', font=("Helvetica", 20))
        self.total_stage_time_label.pack(anchor='center')
    
        self.total_show_time_label = tk.Label(key_info_frame, text=f'Total Show Time: N/A', font=("Helvetica", 20))
        self.total_show_time_label.pack(anchor='center')

        """ -- Next Options -- """
        button_frame = tk.Frame(self)
        button_frame.pack(side='bottom', pady=3)

        # Save Show
        save_show_button = tk.Button(button_frame, text="Save Show", font=("Helvetica", 14),
                                     width=12,
                                     command=controller.save_show
                                     )
        save_show_button.grid(column=0, row=0, padx=5)

        # New Show
        new_show_button = tk.Button(button_frame, text="New Show", font=("Helvetica", 14),
                                    width=12,
                                    command=self.controller.start_new_show
                                    )
        new_show_button.grid(column=1, row=0, padx=5)