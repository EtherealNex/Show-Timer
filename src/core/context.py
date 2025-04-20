# App Context holds all shared states

from src.core.models import * # Import Datastructures needed
from src.core.clock import LocalTime

class AppContext:
    def __init__(self):
        
        # Local time
        self.local_time_update_interval = 10
        self.local_time = LocalTime()

        # Pre Show Calls
        self.pre_show_calls = [] # A list for now, later to be gotten from settings

        # Interval context
        self.settings_interval_count = 1
        self.completed_intervals = 0 

        # Widget window context
        self.settings_window_open = False
        self.show_stats_window_open = False
