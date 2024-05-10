# Test.py
import time
from config_utils import read_config
from itertools import cycle

# Define test data as a list of lists or tuples for consistency
test_data = cycle([
    ["1A3F", "0050", "0050", "0018"],
    ["1B2C", "0060", "0060", "0019"],
    ["1C3D", "0070", "0070", "001A"],
    ["1D4E", "0080", "0080", "001B"],
    ["1E5F", "0090", "0090", "001C"],
    ["1F60", "0100", "0100", "001D"],
])

def get_test_data():
    test_refresh_rate = int(read_config('Test Parameters', 'TestRefreshRate'))
    while True:
        selected_data = next(test_data)
        # Create a dictionary with consistent order
        data = {
            'rpm': selected_data[0],
            'speed': selected_data[1],
            'temp': selected_data[2],
            'pressure': selected_data[3]
        }
        print(f"Generated Test Data: {data}")  # Debug output
        time.sleep(test_refresh_rate / 1000.0)  # Convert ms to seconds
        yield data
