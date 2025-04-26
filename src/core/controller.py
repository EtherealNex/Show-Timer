# The Backend controller for show timer

# Import the window frame views
from src.ui.views.pre_show_view import PreShowView
from src.ui.views.main_show_view import MainShowView
from src.ui.views.interval_view import IntervalView
from src.ui.views.show_end_view import ShowEndView

# Import the pop out window widgets
from src.ui.widgets.setting_window_widget import SettingsWindow
from src.ui.widgets.large_time_widget import TimerWindow

import math

# from src.ui.widgets.large_time_widget # This will be implimented after Show Timer joins the DSManager App.

class AppController:
    def __init__(self, main_window, context):
        self.main_window = main_window
        self.context = context

        # Initilise all frames
        self.pre_show_view = PreShowView(context=self.context, controller=self)
        self.main_show_view = MainShowView(context=self.context, controller=self)
        self.interval_view = IntervalView(context=self.context, controller=self)
        self.show_end_view = ShowEndView(context=self.context, controller=self)

        # Initilise all widgets
        self.settings_widget = SettingsWindow(context=self.context, controller=self)

        self.timer_widget = TimerWindow(context=self.context, controller=self)
        self.timer_widget_updater_id = None

        # Close all the widgets
        self.settings_widget.destroy()
        self.timer_widget.destroy()

    """ -- Frame Changing -- """

    def load_initial_view(self):
        self.pre_show_view.__init__(context=self.context, controller=self)
        self.main_window._set_view(self.pre_show_view)

        # Start the local clock
        self.start_local_clock_updates()


    def change_to_main_show_view(self):
        # End previous segment clocks
        self.stop_local_clock_updates()
        self.stop_interval_timers()
        self.end_call_timer()

        # Refresh the main show frame, determine the next button, set the view 
        self.main_show_view.__init__(context=self.context, controller=self)
        self.main_window._set_view(self.main_show_view)

        # Determine this frames logic
        self.main_show_next_button_setter()

        # Start clocks
        self.start_local_clock_updates()
        self.start_main_show_stopwatch() # This can just call start again as the start function checks to see if we have already started
    

    # Determine what the next frame / logic should be for the next button in the main show
    def main_show_next_button_setter(self):
        if self.context.completed_intervals == self.context.settings_interval_count:
            self.main_show_view.next_segment_button.config(text="End Show", command=self.show_end)
        else:
            self.main_show_view.next_segment_button.config(text="Act Down", command=self.change_to_interval)


    def change_to_interval(self):
        # End previous segment clocks
        self.stop_local_clock_updates()
        self.stop_show_stopclock()

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
        # End previous segment clocks, must be ran while prev segment is the current window
        self.stop_local_clock_updates()
        self.stop_main_show_clocks()

        # Refresh the end of show frame, set the view
        self.show_end_view.__init__(context=self.context, controller=self)
        self.main_window._set_view(self.show_end_view)
    
    """ -- Show Insight Control -- """
    def start_new_show(self):
        # Starting a new show will: 



        # Reinitilise the Context, intern restarting all the timers, and resettings the clocks
        self.stop_all_timers() # Redundant but helpful cleanup
        self.context.reset()

        # go to the main window.
        self.load_initial_view()
    


    def save_show(self):
        ...
        # Saveing the show will automatically start a new show
        self.start_new_show()

    def stop_all_timers(self):
        # This is almost redundancy but ensures a good clean up of clocks
        self.end_call_timer()
        self.stop_main_show_clocks()
        self.stop_interval_timers()
        self.stop_local_clock_updates()


    """ -- Main Show Clocks -- """   
    def start_show_stop(self):
        # Start the show stop clock, No need to start the updater as this is done by the main timer.
        self.context.show_stop_stopwatch.start()
        self.context.show_stop_visible = True # Once a show stop occours, make sure to leave the show stop timer on screen always

        # Update the show stop command
        if hasattr(self.main_window._current_view, 'stop_show_button'):
            self.main_window._current_view.stop_show_button.config(
                text='End Show Stop',
                command = self.stop_show_stopclock
            )

    def stop_show_stopclock(self):
        # Stop the show stop clock, will be called when the user swaps to an interval view.
        self.context.show_stop_stopwatch.stop()

        # Update the show stop command
        if hasattr(self.main_window._current_view, 'stop_show_button'):
            self.main_window._current_view.stop_show_button.config(
                text='Show Stop',
                command = self.start_show_stop
            )

    def start_main_show_stopwatch(self):
        # Starts the main show stopwatch, and calls the view updater
        self.context.main_show_stopwatch.start()
        self._update_main_show_clocks()
    
    def stop_main_show_clocks(self):
        # Stops the main show stopwatch, only occours on show_end
        self.context.main_show_stopwatch.stop()
        self.context.show_stop_stopwatch.stop() # Ensure this stops too

        self.main_window._current_view.after_cancel(self._update_main_show_clocks)
  
    def _update_main_show_clocks(self):
        # Updates all the main window clocks, initally just the show stop timer
        if hasattr(self.main_window._current_view, 'show_stopped_timer_label') and self.context.show_stop_visible:
            self.main_window._current_view.show_stopped_timer_label.config(
                text=self.context.show_stop_stopwatch.get_time(in_centi=True),
                font=("Helvetica", 36, "bold")
            )
        
        if hasattr(self.main_window._current_view, 'main_show_timer_label'):
            self.main_window._current_view.main_show_timer_label.config(
                text=self.context.main_show_stopwatch.get_time(in_centi=True)
            )
        
        self.main_window._current_view.after(self.context.main_show_update_rate, self._update_main_show_clocks)


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


    """ -- Show Call Logic -- """
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


    """ -- Widget Window Logic -- """
    # SETTINGS
    def open_setting_window(self):
        if not self.context.settings_window_open:
            self.context.settings_window_open = True
            self.settings_widget.__init__(context=self.context, controller=self)

    # Manage closing the window
    def on_settings_destory(self, event):
        self.context.settings_window_open = False

    # Large Timer Widget
    def open_timer_window(self):

        if not self.context.timer_window_open:
            self.context.timer_window_open = True
            self.timer_widget.__init__(context=self.context, controller=self)

            self.start_local_clock_timer_widget()
    
    def on_timer_window_destroy(self, event):

        self.stop_local_clock_timer_widget()
        self.context.timer_window_open = False

    def start_local_clock_timer_widget(self):
        if hasattr(self.timer_widget, 'local_timer_label'):
            self._update_local_clock_timer_widget()

    def _update_local_clock_timer_widget(self):

        if hasattr(self.timer_widget, 'local_timer_label'):
            # Get width and height, then calcuate font size
            window_width = self.timer_widget.winfo_width()
            font_size = math.trunc(window_width * 2 / 11)

            self.timer_widget.local_timer_label.config(
                text=self.context.local_time.get_time(),
                font=("Helvetica", font_size)
            )

            self.timer_widget_updater_id = self.timer_widget.after(
                self.context.local_time_update_interval, 
                self._update_local_clock_timer_widget
                )

    def stop_local_clock_timer_widget(self):
        if hasattr(self.timer_widget, 'local_timer_label') and self.timer_widget_updater_id:
            self.timer_widget.after_cancel(self.timer_widget_updater_id)
            self.timer_widget_updater_id = None