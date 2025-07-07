# App Context holds all shared states.

from src.core.models import Call

# Load these seperatly as they may move later on.
from src.core.clock import LocalTime
from src.core.clock import Timer
from src.core.clock import Stopwatch

# Get the JSON handler for reading settings
from src.handlers.json_handler import JSONHandler


class AppContext:
    def __init__(self):
        """ -- Functionality settings -- """
        self.showname = "Placeholder" # Changed by the settings on boot
        self.common_update_interval = 10

        # Local time
        self.local_time = LocalTime()

        # Pre Show Calls
        self.settings_pre_show_calls = [  # SETTINGS TO BE UPDATED 
                                Call(label="Quater", duration=600), # Normally 600 (10m)
                                Call(label="Five", duration=300),
                                Call(label="Begginers", duration=300)
                                ]
        self.current_call_index: int = 0
        self.active_call_timer_object: object | None = Timer(overflow=False)

        # Main Show Stopwatches
        self.main_show_stopwatch: object = Stopwatch()
        self.show_stop_visible = False
        self.show_stop_stopwatch: object = Stopwatch()

        # Interval context
        self.settings_interval_count = 1 # SETTINGS TO BE UPDATED
        self.completed_intervals = 0 
        self.interval_length = 900 # 15 * 60 seconds, SETTINGS TO BE UPDATED

        # Interval timers, Begginers is 5m before the end of the interval
        self.interval_timer = Timer(time=self.interval_length, overflow=True)
        self.interval_begginers_call_timer = Timer(time=(self.interval_length - 300), overflow=False)

        self.interval_amber = "#FFA500" # Amber colour. These are later to be replaced by the settings.
        self.interval_red = "#FF0000" # Red colour

        # Widget window context
        self.settings_window_open = False
        self.timer_window_open = False


        """ -- Insight variables -- """
        # Insight variables contain local time sturctures that tell the program when a clock was started or stopped.

        self.acts_list = [] # A list of when Acts were started and stopped
        self.interval_list = [] # A list of when intervals were started and stopped.

        self.total_show_time: int = 0 # A second value of how long the total timer was.
        self.total_show_stopped_time: int = 0 # A second value of how long the show was stopped for in the end.
        self.total_stage_time: int = 0 # A seconds value of the total stage time, this is subtracting show stops, and the interval.

    def reset(self):
        """The Reset function is used to avoid reinitilising the entire context.
This will prevent issues in the future when things needs to be gotten from the settings.
And allows a tighter easier controll over what is reset when the show timer is reset."""
        
        # Reset Call context
        self.current_call_index = 0
        self.active_call_timer_object.stop()
        self.active_call_timer_object = Timer(overflow=True)

        self.main_show_stopwatch.reset()
        self.show_stop_visible = False
        self.show_stop_stopwatch.reset()

        self.completed_intervals = 0
        self.interval_timer.reset()
        self.interval_begginers_call_timer.reset()

        # Reset insight settings
        self.acts_list.clear()
        self.interval_list.clear()
        self.total_show_time = 0
        self.total_show_stopped_time = 0
        self.total_stage_time = 0

    def get_settings(self, path: str):
        """Takes `path` to read settings from it through the JSON handler"""
        settings_dict, fail_flag = JSONHandler.readSettings(path=path)

        # Set up the settings from the imported dict, the handler will always pass in valid settings, may generate a default.
        # The fail flag is then used to determine what error message to show if any.

        self.showname = settings_dict['showName']

        # Replace the calls with the ones from the settings
        self.settings_pre_show_calls = [
            Call(label=call.get("Name"), duration=call.get("Duration")) 
            for call in settings_dict.get('preShowCall', {}).values()
        ]

        self.settings_interval_count = settings_dict['intervalCount']
        self.interval_length = int(settings_dict['intervalLength'])

        # Replace the timer
        self.interval_timer = Timer(time=self.interval_length, overflow=True)
        self.interval_begginers_call_timer = Timer(time=(self.interval_length - 300), overflow=False)     

        return fail_flag if fail_flag != 0 else 0 # Run the fail messages
