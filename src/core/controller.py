# The Backend controller for show timer

# Import the window frame views
from src.ui.views.pre_show_view import PreShowView
from src.ui.views.main_show_view import MainShowView
from src.ui.views.interval_view import IntervalView
from src.ui.views.show_end_view import ShowEndView

# Import the pop out window widgets
from src.ui.widgets.setting_window_widget import SettingsWindow
from src.ui.widgets.show_stats_widget import ShowStats
# from src.ui.widgets.large_time_widget # This will be implimented after Show Timer joins the DSManager App.

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

        # Start the local clock
        self.start_local_clock_updates()


    def change_to_main_show_view(self):
        # End previous segment clocks
        self.stop_local_clock_updates()

        # Refresh the main show frame, determine the next button, set the view 
        self.main_show_view.__init__(context=self.context, controller=self)
        self.main_window._set_view(self.main_show_view)

        # Determine this frames logic
        self.main_show_next_button_setter()
        self.start_local_clock_updates()
    

    # Determine what the next frame / logic should be for the next button in the main show
    def main_show_next_button_setter(self):
        if self.context.completed_intervals == self.context.settings_interval_count:
            self.main_show_view.next_segment_button.config(text="End Show", command=self.show_end)
        else:
            self.main_show_view.next_segment_button.config(text="Act Down", command=self.change_to_interval)


    def change_to_interval(self):
        # End previous segment clocks
        self.stop_local_clock_updates()

        # Update the context
        self.context.completed_intervals += 1

        # Refresh the interval frame, set the view
        self.interval_view.__init__(context=self.context, controller=self)
        self.main_window._set_view(self.interval_view)

        # Determine this frames logic
        self.start_local_clock_updates()

    def show_end(self):
        # End previous segment clocks
        self.stop_local_clock_updates()

        # Refresh the end of show frame, set the view
        self.show_end_view.__init__(context=self.context, controller=self)
        self.main_window._set_view(self.show_end_view)

    """ --  Local Clock Update Task -- """
    def start_local_clock_updates(self):
        if hasattr(self.main_window._current_view, 'local_timer_label'):
            self._update_local_clock()
    
    def _update_local_clock(self):
        if hasattr(self.main_window._current_view, 'local_timer_label'):
            self.main_window._current_view.local_timer_label.config(
                text=self.context.local_time.get_time()
            )

            # Schedule the next update
            self.main_window._current_view.after(self.context.local_time_update_interval,
                                                 self._update_local_clock
                                                 )
    
    def stop_local_clock_updates(self):
        if hasattr(self.main_window._current_view, 'local_timer_label'):
            self.main_window._current_view.after_cancel(self._update_local_clock)


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

