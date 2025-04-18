# The Backend controller for show timer

from src.ui.views.pre_show_view import PreShowView
from src.ui.views.main_show_view import MainShowView
from src.ui.views.interval_view import IntervalView

from src.ui.widgets.setting_window_widget import SettingsWindow
from src.ui.widgets.show_stats_widget import ShowStats

class AppController:
    def __init__(self, main_window, context):
        self.main_window = main_window
        self.context = context

        # Initilise all frames
        self.pre_show_view = PreShowView(context=context, controller=self)
        self.main_show_view = MainShowView(context=context, controller=self)
        self.interval_view = IntervalView(context=context, controller=self)

    """ -- FRAME CHANGING -- """
    # Set up the intial frame
    def load_initial_view(self):
        self.pre_show_view.__init__(context=self.context, controller=self)
        self.main_window._set_view(self.pre_show_view)

    # Swap to main show frame
    def change_to_main_show_view(self):
        ... # Code for starting the show and other logic
        print("Swapping to main show view")

        # Refresh the main show frame, determine the next button, set the view 
        self.main_show_view.__init__(context=self.context, controller=self)
        self.main_show_next_button_decision()
        self.main_window._set_view(self.main_show_view)
    
    # Determine what the next frame / logic should be for the next button in the main show
    def main_show_next_button_decision(self):
        ... # Logic for determining & setting the button label.

        # For UI dev, just return a start interval
        self.main_show_view.next_segment_button.config(text="Act Down", command=self.change_to_interval)

    def change_to_interval(self):
        ... # Code for starting the interval

        # Refresh the interval frame, set the view
        self.interval_view.__init__(context=self.context, controller=self)
        self.main_window._set_view(self.interval_view)


    """ -- WIDGET WINDOW LOGIC -- """

    # SETTINGS

    #Open the window
    def open_setting_window(self):
        if not self.context.settings_window_open:
            self.context.settings_window_open = True
            settings_window = SettingsWindow(self.context, self)

    # Manage closing the window
    def on_settings_destory(self, event):
        self.context.settings_window_open = False

    # STATS

    # Open the window
    def open_stats_window(self):
        if not self.context.show_stats_window_open:
            self.context.show_stats_window_open = True
            stats_window = ShowStats(self.context, self)

    # Manage Closing the window
    def on_stats_window_destory(self, event):
        self.context.show_stats_window_open = False

