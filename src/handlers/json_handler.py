# JSON Handler will work with the app to save shows and eventually to revist old shows, This will eventually
# be ported and changed into the larger overall app, where we can go back and read all the old shows.
import json, os

class JSONHandler:
    """JSON is a static method based class structure that reads, and writes from json files.
    This implimentation of json handler allows the reading of show data for show timer."""
    
    @staticmethod
    def ShowWrite(path: str, data: dict):
        """Appends a new run to the correct show in the JSON.
        Expects `path` and `data` and all run information, passed in through the controller of the application"""

        show_name = data.get("Show Name") # Determine the show it is appart of
        if not show_name:
            raise ValueError('Missing Show Name, unable to save.')
        
        # Remove the show name as to store relevent information
        run_data = {k: v for k, v in data.items() if k != "Show Name"}

        # Load the existing JSON data, or create a new one if none exists.
        if os.path.exists(path):
            with open(path, "r") as file:
                try:
                    json_data = json.load(file)
                except json.decoder.JSONDecodeError:
                    json_data = {}
                file.close()

        
        else:
            json_data = {}

        # Ensure the show exists
        if show_name not in json_data:
            json_data[show_name] = {}

        # Get the existing run number
        existing_runs = json_data[show_name]
        next_run_number = len(existing_runs) + 1
        run_key = f"Run {next_run_number}"

        # Add the new run
        json_data[show_name][run_key] = run_data

        # Write back to the file
        with open(path, "w") as file:
            json.dump(json_data, file, indent=4)
            file.close()

    @staticmethod
    def readSettings(path:str) -> dict:
        """Reads application settings from the `path` and returns the dictonary of settings for
        later processing.
        
        Fail Flag:
        - 1: File corrupted, or missing data, generating a new settings file.
        - 2: File does not exist, generating a new file"""
        settings_dict = {}
        default_settings = {}

        fail_flag = 0

        # Load the existing file, if none exists, create a new default file.
        if os.path.exists(path):

            with open(path, 'r') as file:
                try:
                    settings_dict = json.load(file)
                    file.close()

                except json.decoder.JSONDecodeError:
                    fail_flag = 1 # File corrupted error

        else: # File doesn't exist, error
            fail_flag = 2

        if fail_flag != 0: # We need to write the defualt settings if anything fails.
            settings_dict = default_settings
            JSONHandler.writeSettings(path=path, settings_data=settings_dict)

        return settings_dict, fail_flag
    
    @staticmethod
    def writeSettings(path: str, settings_data: dict) -> None:
        """Writes passed in dictionary to the settings JSON file. Ensure that entered data contains all correct fields"""
        
        """Fields needed:
        `Show name` - The name of the show file it will save as.
        `pre show calls` - A dictonary of calls, their name, and length in seconds.
        `interval count` - How many intervals the show will run with.
        `interval length` - How long every interval will be.
        """

        with open(path, 'w') as file:
            json.dump(settings_data, file, indent=4)
            file.close()


if __name__ == "__main__":
    testdata = {
        "Show Name": "Hamilton",  # Used to route the data
        "Show Start Time": "18:22222",
        "Show End Time": "20:40",
        "Total Show Time": "2:30",
        "Show Stopped Time": "00:00:00",
        "Acts": {
            "Act 1": {"Start": "18:10", "End": "19:10", "Duration": "1:00"},
            "Act 2": {"Start": "19:30", "End": "20:40", "Duration": "1:10"}
        },
        "Intervals": {
            "Interval 1": {"Start": "19:10", "End": "19:30", "Duration": "0:20"}
        }
    }

    JSONHandler.ShowWrite(path="tests/testing.json", data=testdata)

