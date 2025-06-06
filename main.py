# The main entry point for Show Timer

from src.ui.main_window import MainWindow
from src.core.context import AppContext
from src.core.controller import AppController

def main():
    # Application setup
    context = AppContext()
    app = MainWindow(context=context)
    controller = AppController(main_window=app, context=context)

    # Start the local clock
    context.local_time.start()

    # Set the initial view, then run the mainloop
    controller.load_initial_view()
    app.mainloop()

if __name__ == "__main__":
    main()
