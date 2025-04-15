# App Context holds all shared states

from src.core.clock import LocalTime

class AppContext:
    def __init__(self):
        
        # Local time settings
        self.local_time_update_interval = 250 # in ms
        self.local_time = LocalTime()

        # Widget window context
        self.settings_window_open = False
        self.show_stats_window_open = False
