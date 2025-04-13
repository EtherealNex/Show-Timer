# The main entry point for Show Timer

from src.ui.main_window import MainWindow
from src.core.context import AppContext
from src.core.controller import AppController

def main():
    app = MainWindow()
    context = AppContext()
    controller = AppController(app, context)

    controller.load_initial_view()
    
    app.mainloop()

if __name__ == "__main__":
    main()