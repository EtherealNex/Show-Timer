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
        self.stop_interval_timers()

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

        # Stop, Reset the clocks and then start the interval timers
        self.context.interval_timer.reset()
        self.context.interval_begginers_call_timer.reset()
        self.context.interval_timer.start()
        self.context.interval_begginers_call_timer.start()


        # Refresh the interval frame, set the view
        self.interval_view.__init__(context=self.context, controller=self)
        self.main_window._set_view(self.interval_view)

        # Determine this frames logic
        self.start_local_clock_updates()
        self.start_interval_timer_updates()

    def show_end(self):
        # End previous segment clocks
        self.stop_local_clock_updates()

        # Refresh the end of show frame, set the view
        self.show_end_view.__init__(context=self.context, controller=self)
        self.main_window._set_view(self.show_end_view)

    """ -- Interval Clock Update Task -- """
    def start_interval_timer_updates(self):
        if hasattr(self.main_window._current_view, 'begginers_time_label') and hasattr(self.main_window._current_view, 'interval_timer_label'):
            self._update_interval_timers()
    
    def _update_interval_timers(self):
        if hasattr(self.main_window._current_view, 'begginers_time_label') and hasattr(self.main_window._current_view, 'interval_timer_label'):
            self.main_window._current_view.begginers_time_label.config(
                text=self.context.interval_begginers_call_timer.get_remaining_time(in_centi=False),
                font=("Helvetica", 36)
            )

            self.main_window._current_view.interval_timer_label.config(
                text=self.context.interval_timer.get_remaining_time(in_centi=False)
                )
            
            self.main_window._current_view.after(self.context.interval_update_rate, self._update_interval_timers)

    def stop_interval_timers(self):
        self.context.interval_begginers_call_timer.stop()
        self.context.interval_timer.stop()
        if hasattr(self.main_window._current_view, 'begginers_time_label') and hasattr(self.main_window._current_view, 'interval_timer_label'):
            self.main_window._current_view.after_cancel(self._update_interval_timers)


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


    """ -- SHOW CALL LOGIC -- """
    def load_start_next_call(self):
        # Load the Call timer, increment the call index, move on 

        # Check to see if a call timer is avalible to be used
        if self.context.current_call_index >= len(self.context.settings_pre_show_calls):
            # Update UI
            if hasattr(self.main_window._current_view, 'current_call_label'):
                self.main_window._current_view.current_call_label.config(
                    text=f'No Calls Remaining'
            )
            # Exit Loop
            return
        
        # A call can be done
        self.end_call_timer()
        next_call = self.context.settings_pre_show_calls[self.context.current_call_index]
        self.context.active_call_timer_object.__init__(time=next_call.duration, overflow=False)

        # Set the current call label
        if hasattr(self.main_window._current_view, 'current_call_label'):
            self.main_window._current_view.current_call_label.config(
                text=f'Current Call: {next_call.label}'
            )
        
        # Set the next call label
        if hasattr(self.main_window._current_view, 'next_call_label'):
            if self.context.current_call_index + 1 >= len(self.context.settings_pre_show_calls):
                next_call = "N/A"
            else:
                next_call = f'{(self.context.settings_pre_show_calls[self.context.current_call_index + 1]).label}'
            self.main_window._current_view.next_call_label.config(
                text=f'Next Call: {next_call}'
            )

        self.context.active_call_timer_object.start()
        self.context.current_call_index += 1
        self._update_current_call()

    def _update_current_call(self):
        if hasattr(self.main_window._current_view, 'current_call_timer_lable') and self.context.active_call_timer_object != None:
            self.main_window._current_view.current_call_timer_lable.config(
                text = self.context.active_call_timer_object.get_remaining_time(in_centi=False),
                font=("Helvetica", 36)
        )

            self.main_window._current_view.after(self.context.show_call_update_rate, 
                                                 self._update_current_call)

    def end_call_timer(self):
        self.context.active_call_timer_object.stop()
        if hasattr(self.main_window._current_view, 'current_call_timer_lable'):
            self.main_window._current_view.after_cancel(self._update_current_call)


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

