# The Backend controller for show timer
from src.ui.views.pre_show_view import PreShowView
from src.ui.views.main_show_view import MainShowView

class AppController:
    def __init__(self, main_window, context):
        self.main_window = main_window
        self.context = context

    def load_initial_view(self):
        view = PreShowView(self.context, self)
        self.main_window.set_view(view)

    def start_show(self):
        print("Started Show")
        view = MainShowView(self.context, self)
        self.main_window.set_view(view)
