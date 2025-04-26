# The UI frame for when the show is ended

import tkinter as tk

class ShowEndView(tk.Frame):
    def __init__(self, context, controller):
        super().__init__()
        self.context = context
        self.controller = controller

        """ -- UI -- """
        insights_label = tk.Label(self, text='Show Insights', font=("Helvetica", 36, "bold"))
        insights_label.pack(side='top', pady=5)


        """ -- Next Options -- """
        button_frame = tk.Frame(self)
        button_frame.pack(side='bottom', pady=10)

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