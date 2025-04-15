# The main entry point for Show Timer

from src.ui.main_window import MainWindow
from src.core.context import AppContext
from src.core.controller import AppController

def main():
    app = MainWindow()
    context = AppContext()
    controller = AppController(main_window=app, context=context)

    # Start the local clock
    context.local_time.start()

    # Set the main view
    controller.load_initial_view()
    
    app.mainloop()

if __name__ == "__main__":
    main()

# Local timer must have a way to globalise it as we keep creating a new one for each frame
# Possibly one in context that can be called when needed, and updated by controller
# This would remove the need for it to be managed within each frame

# Manage it in main window? / Context