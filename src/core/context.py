# App Context holds all shared states

from src.core.clock import LocalTime

class AppContext:
    def __init__(self):
        
        # Local time
        self.local_time_update_interval = 250 # in ms
        self.local_time = LocalTime()

        # Interval context
        self.settings_interval_count = 1
        self.completed_intervals = 0 

        # Widget window context
        self.settings_window_open = False
        self.show_stats_window_open = False
