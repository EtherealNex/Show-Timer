# A NexLib Libary for reading and writing JSON files
import json

class JSONHandler:
    def __init__(self, file_path: str | None = None):
        self.file_path = file_path
        self.data = {}
    
    @staticmethod # This can be a static method as it does not need the class
    def read_json(file_path):
        """Reads the JSON file and returns the data as a dictionary."""
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            file.close()
            return data
        
        except FileNotFoundError:
            print(f'Error: The file {file_path} was not found.')
            return None
        except json.JSONDecodeError:
            print(f'Error: The file {file_path} is not a valid JSON file.')
            return None
        except Exception as e:
            print('Error: An unexpected error occurred while reading the JSON file:', e)
            return None

    @staticmethod
    def tk_font(data):
        """Converts the font data from the JSON file to a tkinter font object."""
        try:
            tk_fonts = {}
            for font_name, font_properites in data['fonts'].items():
                tk_fonts[font_name] = (font_properites['fontFamily'],
                                       font_properites['fontSize'],
                                       font_properites['fontWeight'])
            return tk_fonts
        except Exception as e:
            print('Error: An unexpected error occurred while converting the font data:', e)
            return None

    @staticmethod
    def tk_color(data):
        """Converts the color data from the JSON file to a tkinter color object."""
        try:
            tk_colors = {}
            for color_name, color_value in data['colors'].items():
                tk_colors[color_name] = color_value
            return tk_colors
        except Exception as e:
            print('Error: An unexpected error occurred while converting the color data:', e)
            return None

    def write_json(self, data, append=False):
        """Writes the given data to the JSON file. With the option to append or overwrite."""
        try:
            if append:
                # Read existing data
                existing_data = self.read_json(self.file_path)
                if existing_data is not None:
                    existing_data.update(data)
                    data = existing_data

            with open(self.file_path, 'w') as file:
                json.dump(data, file, indent=4)
                print('Data written to JSON file successfully.')
            
        except FileNotFoundError:
            print(f'Error: The file {self.file_path} was not found.')
            return None
        except Exception as e:
            print('Error: An unexpected error occurred while writing to the JSON file:', e)
            return None

if __name__ == "__main__":
    testing = ('src/assets/themes/default_theme.json')
    data = JSONHandler.read_json(testing)


    # Testing getting a specific color from a color name
    color_value = data['colors'].get('backgroundColor')
    print(color_value)
