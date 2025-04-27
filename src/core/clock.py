# @NexLib -> A general libary created by Nex // Heavily modified for Show Timer Efficiancy

import time, threading

class Formatter:
    """A powerfull Time formmatter intended for useage in clock systems."""

    @staticmethod
    def _format(seconds: int | float, include_sign: bool = True):
        """Returns a tuple (sign, hrs, mins, secs, centi) based off of the seconds inputed"""

        # Determine sign and ensure seconds are valid
        if not isinstance(seconds, (int, float)): # All code runs the format through here so all checks can be carried out here
            raise TypeError(f"seconds expected int or float, got {type(seconds).__name__}")

        # Check to insure include sign has been passed in as a bool
        if not isinstance(include_sign, bool): 
            # This isnt used in this function but is a good place to include as all functions must pass throguh this
            # If this is not needed, the system will give it a True bool value to pass this check
            raise TypeError(f'include sign expected bool, got {type(include_sign).__name__}')
        
        sign = '-' if seconds < 0 else ''
        seconds = abs(seconds)
        
        # Calculate values
        hrs = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        centi = int((seconds * 100) % 100)

        return sign, hrs, mins, secs, centi

    @staticmethod
    def format_centi(seconds: int | float, include_sign: bool = True):
        """
        Returns a string formatted time of an input of seconds. 'sign hrs:mins:secs:centi'
        This function will not check to ensure include_sign is a bool value as this is handled by the _format function
        """
        # Get formatted
        sign, hrs, mins, secs, centi = Formatter._format(seconds, include_sign)
        return f'{sign if include_sign else ""}{hrs:02}:{mins:02}:{secs:02}:{centi:02}'
    
    @staticmethod
    def format_secs(seconds: int | float, include_sign: bool = True):
        """
        Returns a string formatted time of an input of seconds. 'sign hrs:mins:secs:centi'
        This function will not check to ensure include_sign is a bool value as this is handled by the _format function
        """
        # Get formatted
        sign, hrs, mins, secs, _ = Formatter._format(seconds, include_sign)
        return f'{sign if include_sign else ""}{hrs:02}:{mins:02}:{secs:02}'

class Clock:
    """The clock superclass that will handle alot of common functionality"""
    @staticmethod
    def get_local_time_struct() -> time.struct_time:
        """Returns a time struct from the time libary"""
        return time.localtime()
    
    @staticmethod
    def get_time_struct_formatted(time_struct: time.struct_time) -> str:
        """Returns the time struct formmatted in HH:MM:SS"""
        return(time.strftime("%H:%M:%S", time_struct))
    
    @staticmethod
    def delta_local_clock_time(time1: time.struct_time, time2: time.struct_time) -> int:
        """delta local clock time will calcuate the time between 2 local time time structures, returning the result as an int repressenting seconds"""
        time1 = time.mktime(time1)
        time2 = time.mktime(time2)
        return int(time2 - time1)

    def __init__(self):
        # Common variables
        self._running = False
        self._start_time = None

        self._lock = threading.Lock()

        # // Added for Show Timer
        self.record_start = None
        self.record_stop = None
    
    def start(self):
        """Sets up the starting variables and creates the thread to run the clock on"""
        if not self._running:
            # Set the starting variables
            self._running = True
            self.record_start = time.localtime()

            # Start the thread
            self._update_thread = threading.Thread(target=self._update, daemon=True)
            self._update_thread.start()
    
    def stop(self):
        self._running = False
        self._start_time = None
        self._update_thread.join()
        self.record_stop = time.localtime()
    
    def _update(self):
        """Update code must be individualy created for each class that inherits the clock functionality"""
        raise ProcessLookupError(f"""The update function must be created for each class that inherits the Clock.
                                 If you are using this app, please contact the developer.""")
            
    def reset(self):
        self._running = False
        self._start_time = None
        self.record_start = None
        self.record_stop = None

    def start_end_local(self):
        try:
            return [time.strftime("%H:%M:%S", self.record_start), time.strftime("%H:%M:%S", self.record_stop)]
        except TypeError:
            return None
        except Exception as e:
            return e

class Stopwatch(Clock):
    """
    A stopwatch that will create a new thread to be ran on keeping your main program running smoothly.
    This clock will tick up.

    Takes a update rate, set to 0.01 seconds by defult
    """
    def __init__(self, update_rate: int | float = 0.01):
        super().__init__()

        if not isinstance(update_rate, (int, float)): # Error handling when not int or float inputted
            raise TypeError(f'Update rate expected an int or float, got {type(update_rate).__name__}')
        
        self.update_rate = update_rate
        self._elapsed_time = 0
    
    def _update(self):
        """Updates the stopwatch by getting the time, and subtractig the start time, then waits the update time, then calls itself again"""
        # Set the threads name
        self._update_thread.name = f"Stopwatch: {id(self)}"
        while self._running:
            # Lock the thread, then Get current time, set the elapsed to time since start
            with self._lock:
                current_time = time.time()
                self._elapsed_time = (current_time - self._start_time)

            # wait the update_rate, then recursion
            time.sleep(self.update_rate)
    def start(self):
        self._start_time = time.time() - self._elapsed_time
        super().start()

    def stop(self):
        """
        Stops the stopwatch, sets the elapsed time to the true value, records the stop time.
        """
        if self._running:
            with self._lock:
                current_time = time.time()
                self._elapsed_time = (current_time - self._start_time)
                super().stop()


    def reset(self):
        """Stops the timer, resets elapsed time, starting time, recorded start, and recorded stopping time"""
        with self._lock:
            super().reset()
            self._elapsed_time = 0

    def get_running(self):
        """A getter for the running variable"""
        return self._running

    def get_time(self, in_centi: bool = True):
        """Gets the elapsed time in centi or seconds depending on input, defults to returning in centi"""
        if not isinstance(in_centi, bool):
            raise TypeError(f"in_centi expected bool, but got {type(in_centi).__name__}")
        return Formatter.format_centi(self._elapsed_time) if in_centi else Formatter.format_secs(self._elapsed_time)
    
    def get_time_in_seconds(self):
        return self._elapsed_time
    
class Timer(Clock):
    """
    A Timer that is created on a new thread to be ran to keep your main program running smoothly
    
    A Timer that counts down from an input second value. And can overflow to continue counting down or stop.

    Takes a second integer or float, set to 300s (5m) by defult.
    Takes an overflow bool, set to True by defult.
    Takes an update_rate, set to 0.01 by defult
    """
    def __init__(self, time: int | float = 300, overflow: bool = True, update_rate: int | float = 0.01):
        super().__init__()

        # Checks
        if not isinstance(time, (int, float)):
            raise TypeError(f'Time expected int or float, got {type(time).__name__}')
        if not isinstance(overflow, bool):
            raise TypeError(f'Overflow expected bool, got {type(overflow).__name__}')
        if not isinstance(update_rate, (int, float)):
            raise TypeError(f'Update rate expected int or float, got {type(update_rate).__name__}')
        
        # When checks passed
        self._duration = time
        self.update_rate = update_rate
        self.overflow = overflow 

        self._remaining_time = self._duration
    
    def _update(self):
        """
        Updates the timer by taking the duration of the clock and subtracting how long its been since starting
        Also handles over flow
        if overflow we continue, else we stop the timer
        """
        self._update_thread.name = f'Timer: {id(self)}'
        epsilon = self.update_rate # The smallest tollerance for the program to ensure we dont have bad floating point subtraction
        while self._running:
            with self._lock:
                current_time = time.time()
                self._remaining_time = self._duration - (current_time - self._start_time)

                if self._remaining_time <= 0 and not self.overflow:
                    self._remaining_time = 0
                    self._running = False
                    break
    
            time.sleep(self.update_rate)

    def start(self):
        self._start_time = time.time()
        super().start()


    def stop(self):
        if self._running:
            with self._lock:
                self._remaining_time = self._duration - (time.time() - self._start_time) # Get absolute remaining time
                super().stop()

    def reset(self) -> None:
        with self._lock:
            super().reset()
            self._remaining_time = self._duration

    def get_remaining_time(self, in_centi: bool = True):
        """Gets the remaining time in centi or seconds depending on input, defults to returning in centi"""
        if not isinstance(in_centi, bool):
            return TypeError(f'in_centi expected bool, got {type(in_centi).__name__}')
        return Formatter.format_centi(self._remaining_time) if in_centi else Formatter.format_secs(self._remaining_time)
        
    def get_real_remaining_time(self) -> int | float:
        return self._remaining_time # Returns seconds of remaing time

    def get_running(self):
        return self._running

class LocalTime:
    def __init__(self, update_rate: int | float = 0.75):
        self._running = False
        self._current_time = time.localtime()

        self._lock = threading.Lock()
        self._last_formatted_time = ""

        if not isinstance(update_rate, (int, float)):
            raise TypeError(f'Update rate expected int or float, got {type(update_rate).__name__}')
        else:   self.update_rate = update_rate

    def start(self):
        if not self._running:
            self._running = True
            self._update_thread = threading.Thread(target=self._update, daemon=True)
            self._update_thread.name = f"Local clock {id(self)}"
            self._update_thread.start()
        
    def _update(self):
        while self._running:
            with self._lock:
                self._current_time = time.localtime()
                self._last_formatted_time = time.strftime("%H:%M:%S", self._current_time)

            time.sleep(self.update_rate)
    
    def stop(self):
        self._running = False
    
    def get_time(self, in_centi: bool = False):
        """Returns a formatted time for the local time.
        By default, it returns time in seconds, with an option to include centiseconds."""
        if not isinstance(in_centi, bool):
            raise TypeError(f'in_centi expected bool, got {type(in_centi).__name__}')
        
        with self._lock:
            return(time.strftime("%H:%M:%S",time.localtime()))
            #return self._last_formatted_time

if __name__ == "__main__":
    # Test the stopwatch
    test_stopwatch = False
    test_timer = False
    test_local = False

    if test_stopwatch:

        stop = Stopwatch()
        stop.start()

        time.sleep(3.23)  # Let the stopwatch run for 1 second
        print(f"Running: {stop.get_running()}")
        print(f"Elapsed Time (centi): {stop.get_time()}")
        print(f"Elapsed Time (seconds): {stop.get_time(False)}")

        time.sleep(2.31)
        print(f"Running: {stop.get_running()}")
        print(f"Elapsed Time (centi): {stop.get_time()}")
        print(f"Elapsed Time (seconds): {stop.get_time(False)}")

        stop.stop()
        print(f"Running: {stop.get_running()}")
        print(f"Final Time: {stop.get_time()}")

        stop.reset()
        print(f"Running: {stop.get_running()}")
        print(f"Time After Reset: {stop.get_time()}")
    
    if test_timer:
        timer = Timer(time=5, overflow=True, update_rate=0.5)
        timer.start()

        # Print the initial value
        with timer._lock:
            print(f'Remaining Time: {Formatter.format_secs(timer.get_real_remaining_time())}')

        while timer._running:
            with timer._lock:
                print(f'Remaining Time: {Formatter.format_secs(timer.get_real_remaining_time())}')
            time.sleep(0.1)

        print("Timer Finished!")

    if test_local:
        local = LocalTime()
        local.start()
        try:
            for _ in range(5):  # Print local time 5 times
                print(f'Local Time: {local.get_time()}')
                time.sleep(1)
        finally:
            local.stop()