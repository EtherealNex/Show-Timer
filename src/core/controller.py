# The Backend controller for show timer

# Import the window frame views
from src.ui.views.pre_show_view import PreShowView
from src.ui.views.main_show_view import MainShowView
from src.ui.views.interval_view import IntervalView
from src.ui.views.show_end_view import ShowEndView

# Import the pop out window widgets
from src.ui.widgets.setting_window_widget import SettingsWindow
from src.ui.widgets.large_time_widget import TimerWindow
from src.ui.widgets.alert import alert

from src.core.models import Call

from src.core.clock import Clock, Formatter
from src.handlers.json_handler import JSONHandler
import math, ast, tkinter as tk

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

        # Now everything has been initilised, we can get the settings, this way, 
        # we can also trigger alert functions from here depending on the situation

        failed = self.context.get_settings("userdata/show_settings.json") # This will also cause the settings to apply
        if failed != 0: # An error has occoured, we must now check the error and return an alert.
            self.get_alert(fail_flag=failed) # This will run the alert box to show a error of getting settings

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

        # Ensure that the settings window is closed to prevent user changing settings mid show
        if self.context.settings_window_open:
            self.settings_widget.destroy()

        # Whenever we go to the main show view we want to append the local time to the context array
        self.context.acts_list.append(Clock.get_local_time_struct())

        # We want to append an interval end time to the context, but only if the interval was actually triggered and not on the start of the show
        if self.context.completed_intervals != 0: # If we have Finsihed an interval
            self.context.interval_list.append(Clock.get_local_time_struct())

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
        if int(self.context.completed_intervals) >= int(self.context.settings_interval_count):
            self.main_show_view.next_segment_button.config(text="End Show", command=self.show_end)
        else:
            self.main_show_view.next_segment_button.config(text="Act Down", command=self.change_to_interval)

    def change_to_interval(self):
        # End previous segment clocks
        self.stop_local_clock_updates()
        self.stop_show_stopclock()

        # Append the local time to the acts list in context
        self.context.acts_list.append(Clock.get_local_time_struct())

        # We want to append the time we went to the interval to the context whenever we go here
        self.context.interval_list.append(Clock.get_local_time_struct())

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

        # Finally append an ending show time to context to make sure the acts list is even.
        self.context.acts_list.append(Clock.get_local_time_struct())

        # Set show context for final timers
        self.context.total_show_time = self.context.main_show_stopwatch.get_time_in_seconds()
        self.context.total_show_stopped_time = self.context.show_stop_stopwatch.get_time_in_seconds()

        # Calculate the total stage time
        # Take the Total Time, Subtract the show stopped time
        self.context.total_stage_time = self.context.total_show_time - self.context.total_show_stopped_time
        # Take this new time and itterate through the intervals subtracting their time
        for i in range(0, len(self.context.interval_list) - 1, 2): #e.g, time1, time2, time3, time4
            interval_start = self.context.interval_list[i]
            interval_end = self.context.interval_list[i + 1]
            
            interval_length = Clock.delta_local_clock_time(interval_start, interval_end)
            self.context.total_stage_time -= interval_length
            

        # Refresh the end of show frame, set the view
        self.show_end_view.__init__(context=self.context, controller=self)

        # Building the insight data
        self.determine_insights()
        self.main_window._set_view(self.show_end_view)


        # Set the key info text
        if hasattr(self.main_window._current_view, 'total_show_stop_time_label'):
            self.main_window._current_view.total_show_stop_time_label.config(
                text=f'Show Stopped Time: {Formatter.format_centi(self.context.total_show_stopped_time)}'
            )
        
        if hasattr(self.main_window._current_view, 'total_stage_time_label'):
            self.main_window._current_view.total_stage_time_label.config(
                text=f'Total Stage Time: {Formatter.format_centi(self.context.total_stage_time)}'
            )
        
        if hasattr(self.main_window._current_view, 'total_show_time_label'):
            self.main_window._current_view.total_show_time_label.config(
                text=f'Total Show Time: {Formatter.format_centi(self.context.total_show_time)}'
            )


        if hasattr(self.main_window._current_view, 'show_start_stop_local_time_label'):
            show_start = Clock.get_time_struct_formatted(self.context.acts_list[0])
            show_end = Clock.get_time_struct_formatted(self.context.acts_list[-1])
            self.main_window._current_view.show_start_stop_local_time_label.config(
                text=f'Start: {show_start} | End: {show_end}'
            )
    
    """ -- Show Insight Control -- """
    def start_new_show(self):
        # Starting a new show will: 
        # Reinitilise the Context, intern restarting all the timers, and resettings the clocks
        self.stop_all_timers() # Redundant but helpful cleanup
        self.context.reset()

        # go to the main window.
        self.load_initial_view()

    def save_show(self):
        # This func will be updated in the furture to start creating a show report when we get to the full application, 
        # for now it will just save the show to a JSON file, but later this functionality will be expanded.

        """This Function Will Save:

            - Show Name (Settings)
            - Show Run (Calculated based off of previously saved shows)

            - Show Start Time
            - Show End Time
            - Total Show Time
            - Show Stopped Time
            - Show Stopped Time

            - Each Act's Start and End, And Duration
            - Each Intervals Start, End, And Duration
        
        These will be stored to a JSON file within the userdata.
        """  
        
        show_start = Clock.get_time_struct_formatted(self.context.acts_list[0])
        show_end = Clock.get_time_struct_formatted(self.context.acts_list[-1])

        show_data = {
        "Show Name": f"{self.context.showname}",  # Used to route the data
        "Show Start Time": f"{show_start}",
        "Show End Time": f"{show_end}",
        "Total Show Time": f"{Formatter.format_centi(self.context.total_show_time)}",
        "Show Stopped Time": f"{Formatter.format_centi(self.context.total_show_stopped_time)}",
        "Acts": {},  
        "Intervals": {}
        }

        INSIGHT_COUNT = (int(self.context.settings_interval_count) * 2) + 1
        act_index = 0
        interval_index = 0
        
        for i in range(INSIGHT_COUNT):
            if i % 2 == 0: # We are handling ACT data
                # ACT
                act_number = i // 2+1
                start_time = self.context.acts_list[act_index]
                end_time = self.context.acts_list[act_index + 1]
                act_index += 2

                show_data['Acts'][f'Act {act_number}'] = {
                    "Start" : Clock.get_time_struct_formatted(start_time),
                    "End"   : Clock.get_time_struct_formatted(end_time),
                    "Duration" : Formatter.format_secs(Clock.delta_local_clock_time(start_time, end_time))
                }

            else: # We are handling Interval Data
                interval_number = i // 2 + 1
                name = f'Interval {interval_number}' if int(self.context.settings_interval_count) > 1 else "Interval"

                start_time = self.context.interval_list[interval_index]
                end_time = self.context.interval_list[interval_index + 1]
                interval_index += 2

                show_data['Intervals'][name] = {
                    "Start" : Clock.get_time_struct_formatted(start_time),
                    "End"   : Clock.get_time_struct_formatted(end_time),
                    "Duration" : Formatter.format_secs(Clock.delta_local_clock_time(start_time, end_time))
                }

        # Save the show to the user data file
        JSONHandler.ShowWrite("userdata/show_insights.json", show_data)

        # Saveing the show will automatically start a new show
        self.start_new_show()

    def stop_all_timers(self):
        # This is almost redundancy but ensures a good clean up of clocks
        self.end_call_timer()
        self.stop_main_show_clocks()
        self.stop_interval_timers()
        self.stop_local_clock_updates()

    def determine_insights(self):

        # Calculate how many insights there should be bassed off of the interval count
        INSIGHT_COUNT = (int(self.context.settings_interval_count) * 2) + 1
        
        # Track acts and intervals
        act_index = 0
        interval_index = 0

        # Itterate through the insight count 
        for i in range(INSIGHT_COUNT):
            # Calculate act or interval
            if i % 2 == 0: # Even index == Act
                name = f'Act {i // 2 + 1}:'
                start_time = (self.context.acts_list[act_index])
                end_time = (self.context.acts_list[act_index + 1])
                act_index += 2 # Skip the 2 we have already done

            else: # Odd == Interval
                name = f'Interval {i // 2 + 1}:' if int(self.context.settings_interval_count) > 1 else f'Interval:'
                start_time = self.context.interval_list[interval_index]
                end_time = self.context.interval_list[interval_index + 1]
                interval_index += 2


            start_time_str = Clock.get_time_struct_formatted(start_time)
            end_time_str = Clock.get_time_struct_formatted(end_time)

            deltatime = Clock.delta_local_clock_time(start_time, end_time)
            deltatime_str = Formatter.format_secs(deltatime)

            frame = self.build_insight_frame(self.show_end_view.show_data_frame, f'{name}', start_time_str, end_time_str, deltatime_str)
            frame.pack(fill='x', padx=5)
            self.show_end_view.canvas.configure(scrollregion=self.show_end_view.canvas.bbox("all"))

    def build_insight_frame(self, parent_frame: tk.Frame, title: str, start: str, end: str, deltatime: str):
        """ Build the frame that gets appended to the insights page """

        insight_frame = tk.Frame(parent_frame)
        insight_frame.pack(fill='x', expand=True) 

        # Now pack the labels inside the insight_frame
        tk.Label(insight_frame, text=f'{title}', font=("Helvetica", 24)).pack(anchor='w', padx=20)  # Left aligned
        tk.Label(insight_frame, text=f'Start: {start} | End: {end}', font=("Helvetica", 20)).pack(anchor='center', padx=40)  # Centered
        tk.Label(insight_frame, text=f'{deltatime}', font=("Helvetica", 20)).pack(anchor='center', padx=40)  # Centered

        return insight_frame

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
        
        self.main_window._current_view.after(self.context.common_update_interval, self._update_main_show_clocks)


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
            
            # If the interval timer gets below 300s, change the BG to amber, if below 0 change to red
            if self.context.interval_timer.get_real_remaining_time() < 300: # Only run bg update code if below 5m 
                # Determine the colour
                colour = self.context.interval_red if self.context.interval_timer.get_real_remaining_time() < 0 else self.context.interval_amber
                # Change all BG's to amber except the interval timer and local clock
                self.main_window._current_view.configure(background=colour)
                self.main_window._current_view.begginers_time_label.configure(background=colour)
                self.main_window._current_view.begginers_label.configure(background=colour)
                self.main_window._current_view.end_interval_button.config(highlightbackground=colour, background=colour)

                # Give the main interval timer and local clock a border
                self.main_window._current_view.center_frame.config(borderwidth=3, relief='solid')
            
            self.main_window._current_view.after(self.context.common_update_interval, self._update_interval_timers)

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
            self.main_window._current_view.after(self.context.common_update_interval,
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

            self.main_window._current_view.after(self.context.common_update_interval, 
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
            window_height = self.timer_widget.winfo_height()
            font_size = math.trunc(int(0.3 * (window_width * window_height) ** 0.5))

            self.timer_widget.local_timer_label.config(
                text=self.context.local_time.get_time(),
                font=("Helvetica", font_size)
            )

            self.timer_widget_updater_id = self.timer_widget.after(
                self.context.common_update_interval, 
                self._update_local_clock_timer_widget
                )

    def stop_local_clock_timer_widget(self):
        if hasattr(self.timer_widget, 'local_timer_label') and self.timer_widget_updater_id:
            self.timer_widget.after_cancel(self.timer_widget_updater_id)
            self.timer_widget_updater_id = None

    """ -- Settings Logic -- """
    def save_settings(self):
        showName, preShowCall, intervalCount, intervalLength = self.get_settings()
        settings = {
            "showName" : f"{showName}",

            "preShowCall" : self.convert_call_to_json(preShowCall),

            "intervalCount" : intervalCount,
            "intervalLength": intervalLength
        }
        if preShowCall == False:
            settings = {} # Will raise a write error
        write_fail = JSONHandler.writeSettings("userdata/show_settings.json", settings)

        if write_fail != 0:
            self.get_alert(write_fail)
            return
        else: # Success, update the settings again
            self.context.get_settings(path="userdata/show_settings.json")

        # Saving will close the settings window
        if self.context.settings_window_open:
            self.settings_widget.destroy()

    def get_settings(self):
        """Gets the settings from the GUI input box's, returns all the needed variables"""
        
        if hasattr(self.settings_widget, "show_name_entry"):
            showName = self.settings_widget.show_name_entry.get()

        if hasattr(self.settings_widget, "interval_count_entry"):
            intervalCount = self.settings_widget.interval_count_entry.get()
        
        if hasattr(self.settings_widget, "interval_duration_entry"):
            intervalLength = self.settings_widget.interval_duration_entry.get()
        
        if hasattr(self.settings_widget, "show_call_entry"):
            preShowCall_text = self.settings_widget.show_call_entry.get("1.0", tk.END).strip()

            try:
                preShowCall = []
                parsed = ast.literal_eval(f'[{preShowCall_text}]')
                
                if not isinstance(parsed, list):
                    return False, False, False, False
                
                for item in parsed:
                    if not (isinstance(item, tuple) and len(item) == 2):
                        return False, False, False, False
                    lable, duration = item
                    if not (isinstance(lable, str) or not isinstance(duration, int)):
                        return False, False, False, False
                    preShowCall.append(Call(label=lable, duration=duration))

            except Exception as e:
                raise ValueError(f'Failed to parse: {e}')

        return showName, preShowCall, intervalCount, intervalLength
    
    def convert_call_to_json(self, call_list):
        pre_show_call = {}

        for i, call in enumerate(call_list, start=1):
            key = f'Call {i}'
            pre_show_call[key] = {
                "Name" : call.label,
                "Duration" : call.duration
            }
        return pre_show_call

    def get_calls_as_text(self):
        call_tuples = [(call.label, call.duration) for call in self.context.settings_pre_show_calls]
        return ', '.join(f'("{label}", {duration})' for label, duration in call_tuples)


    """ -- Alert Functionality -- """
    def get_alert(self, fail_flag) -> None:
        """`fail_flag` will determine what error message is shown"""
        error_message = "Placeholder"

        match fail_flag:
            # Reading Settings Error
            case 100:
                error_message = "ERROR: Settings File Corrupted or Missing Data. Reset Settings to Defaults."
            case 101:
                error_message = "ERROR: Settings File Does Not Exist. Generated file, Reset to Defaults."
            
            # Writing Settings Error
            case 200:
                error_message = "ERROR: Unable to save settings due to missing or invalid values."

            # Default Case
            case _:
                error_message = "ERROR: Unknown error please contact."

        alert(message=error_message, title="ERROR")