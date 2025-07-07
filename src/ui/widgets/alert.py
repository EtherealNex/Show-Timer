# This is a customisable, alert tkinter widget, it is called within the program where needed and creates 
# a new window with the alert text and a simple close button, this is good for when an error has arrised, 
# as staying away from console driven program.

import tkinter as tk

def alert(message: str, title: str = "Alert", size: str = "300x100", resiasable: bool = False):
    # Create the alert window
    window = tk.Toplevel() # Place the window ontop of everything
    window.title(title)
    window.resizable(resiasable, resiasable)

    window.attributes('-topmost', True) # Force it to appear at the top level

    window.geometry(size)

    # Label for alert text
    alert_text_label = tk.Label(window, text=message, padx=10, pady=10, wraplength=280, font=('Helvetica', 16))
    alert_text_label.pack(expand=True)

    # Add a dismiss button
    button = tk.Button(window, text="Ok", command=window.destroy)
    button.pack(pady=(0,10), side='bottom')

    # Ensure the window is modal (cannot interact with other windows)
    window.grab_set()
    window.focus_force()

    # Clean up window close
    window.protocol("WM_DELETE_WINDOW", window.destroy)


