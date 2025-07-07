# A popout widget that controls the timers settings
# This settings widget wont be here in the larger app as that will be controlled globaly, however for now this is here
# When this goes it will be replaced by the large_time_widget.py

import tkinter as tk

class SettingsWindow(tk.Tk):
    def __init__(self, context, controller):
        super().__init__()
        self.context = context
        self.controller = controller

        self.geometry("450x450")
        self.resizable(False, False)
        self.title("Show Timer Settings")

        # When the window is closed, allow it to reopen again
        self.bind("<Destroy>", controller.on_settings_destory)

        """ -- UI CODE -- """

        header_label = tk.Label(self, text='Settings', font=("Helvetica", 30))
        header_label.pack(anchor='center', pady=10)

        show_name_label = tk.Label(self, text="Show Name:", font=('Helvetica', 16, 'bold'))
        show_name_label.pack(pady=5, anchor='w', padx=20)

        self.show_name_entry = tk.Entry(self, width=20, justify='center', font=('Helvetica', 16))
        self.show_name_entry.pack()
        self.show_name_entry.insert(0, self.context.showname)

        interval_count_label = tk.Label(self, text="Interval Count:", font=('Helvetica', 16, 'bold'))
        interval_count_label.pack(pady=5, anchor='w', padx=20)

        self.interval_count_entry = tk.Entry(self, width=20, justify='center', font=('Helvetica', 16))
        self.interval_count_entry.pack()
        self.interval_count_entry.insert(0, self.context.settings_interval_count)

        interval_length_label = tk.Label(self, text="Interval Duration:", font=('Helvetica', 16, 'bold'))
        interval_length_label.pack(pady=5, anchor='w', padx=20)

        self.interval_duration_entry = tk.Entry(self, width=20, justify='center', font=('Helvetica', 16))
        self.interval_duration_entry.pack()
        self.interval_duration_entry.insert(0, self.context.interval_length)

        show_call_label = tk.Label(self, text="Pre Show Calls:", font=('Helvetica', 16, 'bold'))
        show_call_label.pack(pady=5, anchor='w', padx=20)

        self.show_call_entry = tk.Text(self, width=45, height=4, font=('Helvetica', 16))
        self.show_call_entry.pack()
        self.show_call_entry.insert(tk.END, self.controller.get_calls_as_text())


        """ -- Buttons -- """
        button_frame = tk.Frame(self)
        button_frame.pack(side='bottom', pady=6)

        save_button = tk.Button(button_frame, text="Save",
                                font=('Helvetica', 14), width=12,
                                command=self.controller.save_settings)
        save_button.grid(column=0, row=0, padx=15)
