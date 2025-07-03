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
                json_data = json.load(file)
        
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

