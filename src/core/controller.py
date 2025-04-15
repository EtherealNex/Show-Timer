# The Backend controller for show timer

from src.ui.views.pre_show_view import PreShowView
from src.ui.views.main_show_view import MainShowView

from src.ui.widgets.setting_window_widget import SettingsWindow
from src.ui.widgets.show_stats_widget import ShowStats

class AppController:
    def __init__(self, main_window, context):
        self.main_window = main_window
        self.context = context

        # Initilise all windows
        self.pre_show_view = PreShowView(context=context, controller=self)
        self.main_show_view = MainShowView(context=context, controller=self)

    """ -- SETUP INIT WINDOW -- """
    def load_initial_view(self):
        """Sets the applications UI to the initial state"""
        self.main_window._set_view(self.pre_show_view)


    """ -- SETTINGS WINDOW -- """
    #Open the window
    def open_setting_window(self):
        if not self.context.settings_window_open:
            self.context.settings_window_open = True
            settings_window = SettingsWindow(self.context, self)

    # Manage closing the window
    def on_settings_destory(self, event):
        self.context.settings_window_open = False


    """ -- STATS WINDOW -- """
    # Open the window
    def open_stats_window(self):
        if not self.context.show_stats_window_open:
            self.context.show_stats_window_open = True
            stats_window = ShowStats(self.context, self)

    # Manage Closing the window
    def on_stats_window_destory(self, event):
        self.context.show_stats_window_open = False

