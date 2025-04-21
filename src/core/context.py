# App Context holds all shared states

from src.core.models import Call

from src.core.clock import LocalTime
from src.core.clock import Timer

class AppContext:
    def __init__(self):
        
        # Local time
        self.local_time_update_interval = 10
        self.local_time = LocalTime()

        # Pre Show Calls
        self.show_call_update_rate = 10
        self.settings_pre_show_calls = [  # SETTINGS TO BE UPDATED 
                                Call(label="Quater", duration=10), # Normally 600
                                Call(label="Five", duration=300),
                                Call(label="Begginers", duration=10)
                                ]
        self.current_call_index = 0
        self.active_call_timer_object: object | None = Timer(overflow=False)

        # Interval context
        self.settings_interval_count = 1 # SETTINGS TO BE UPDATED
        self.completed_intervals = 0 

        # Widget window context
        self.settings_window_open = False
        self.show_stats_window_open = False
