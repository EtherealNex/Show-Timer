# App Context holds all shared states.

from src.core.models import Call

# Load these seperatly as they may move later on.
from src.core.clock import LocalTime
from src.core.clock import Timer
from src.core.clock import Stopwatch


class AppContext:
    def __init__(self):
        
        # Local time
        self.local_time_update_interval = 10
        self.local_time = LocalTime()

        # Pre Show Calls
        self.show_call_update_rate = 10
        
        self.settings_pre_show_calls = [  # SETTINGS TO BE UPDATED 
                                Call(label="Quater", duration=600), # Normally 600 (10m)
                                Call(label="Five", duration=300),
                                Call(label="Begginers", duration=300)
                                ]
        
        self.current_call_index: int = 0
        self.active_call_timer_object: object | None = Timer(overflow=False)

        # Main Show Stopwatches
        self.main_show_update_rate = 10

        self.main_show_stopwatch: object = Stopwatch()

        self.show_stop_visible = False
        self.show_stop_stopwatch: object = Stopwatch()

        # Interval context
        self.settings_interval_count = 1 # SETTINGS TO BE UPDATED
        self.completed_intervals = 0 

        self.interval_update_rate = 10
        self.interval_length = 900 # 15 * 60 seconds, SETTINGS TO BE UPDATED

        # Interval timers, Begginers is 5m before the end of the interval
        self.interval_timer = Timer(time=self.interval_length, overflow=True)
        self.interval_begginers_call_timer = Timer(time=(self.interval_length - 300), overflow=False)

        # Widget window context
        self.settings_window_open = False
        self.timer_window_open = False

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

