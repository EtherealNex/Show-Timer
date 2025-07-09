# Linker between main app and show timer

"""This for now is a standalone launcher that can be called to generate a new instance of Show Timer

-- THIS IS NOT AN ENTRY POINT --

NOTE: For the standalone github repo, this will serve no use. For the main app this code will change. this is here
for upgradability and future proofing.

NOTE: Show Timer as it stands is not the complete application, there is more to add and revamp code wise.
for example, the controller should be seperated into more files for each of its functionality,
the context should remove logic seperating it further, all these are planned for the main project."""

# Core Imports
from src.ui.main_window import MainWindow
from src.core.context import AppContext
from src.core.controller import AppController


class ShowTimerApp:
    def __init__(self):
        # Application setup
        self.context = AppContext()
        self.app_window = MainWindow(context=self.context)
        self.controller = AppController(main_window=self.app_window, context=self.context)
    
    def run(self):
        # Start the local clock for the app
        self.context.local_time.start()
        """NOTE: This is to be replaced with the overarching clock of the main app"""

        # Load the intial view and start the mainloop
        self.controller.load_initial_view()
        self.app_window.mainloop()

if __name__ == "__main__":
    app = ShowTimerApp()
    app.run()