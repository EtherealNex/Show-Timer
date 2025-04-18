# The Backend controller for show timer

from src.ui.views.pre_show_view import PreShowView
from src.ui.views.main_show_view import MainShowView
from src.ui.views.interval_view import IntervalView
from src.ui.views.show_end_view import ShowEndView

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
        self.show_end_view = ShowEndView(context=context, controller=self)

    """ -- FRAME CHANGING -- """

    def load_initial_view(self):
        self.pre_show_view.__init__(context=self.context, controller=self)
        self.main_window._set_view(self.pre_show_view)


    def change_to_main_show_view(self):
        ... # Code for starting the show and other logic

        # Refresh the main show frame, determine the next button, set the view 
        self.main_show_view.__init__(context=self.context, controller=self)
        # TEST
        self.main_show_next_button_setter()
        self.main_window._set_view(self.main_show_view)
    

    # Determine what the next frame / logic should be for the next button in the main show
    def main_show_next_button_setter(self):
        if self.context.completed_intervals == self.context.settings_interval_count:
            self.main_show_view.next_segment_button.config(text="End Show", command=self.show_end)
        else:
            self.main_show_view.next_segment_button.config(text="Act Down", command=self.change_to_interval)


    def change_to_interval(self):
        ... # Code for starting the interval

        # Update the context
        self.context.completed_intervals += 1

        # Refresh the interval frame, set the view
        self.interval_view.__init__(context=self.context, controller=self)
        self.main_window._set_view(self.interval_view)

    def show_end(self):
        ... # Code to end the show

        # Refresh the end of show frame, set the view
        self.show_end_view.__init__(context=self.context, controller=self)
        self.main_window._set_view(self.show_end_view)

    """ -- WIDGET WINDOW LOGIC -- """

    # SETTINGS
    def open_setting_window(self):
        if not self.context.settings_window_open:
            self.context.settings_window_open = True
            settings_window = SettingsWindow(self.context, self)

    # Manage closing the window
    def on_settings_destory(self, event):
        self.context.settings_window_open = False

    # STATS
    def open_stats_window(self):
        if not self.context.show_stats_window_open:
            self.context.show_stats_window_open = True
            stats_window = ShowStats(self.context, self)

    # Manage Closing the window
    def on_stats_window_destory(self, event):
        self.context.show_stats_window_open = False

