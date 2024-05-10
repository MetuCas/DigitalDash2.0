# This module will emulate serial input by providing test hexadecimal data

# Test.py
import time
from config_utils import read_config
from itertools import cycle

test_data = [
    {"rpm": "1A3F", "speed": "0050", "temp": "0050", "pressure": "0018",}
    {"rpm": "1B2C", "speed": "0060", "temp": "0060", "pressure": "0019",}
    {"rpm": "1C3D", "speed": "0070", "temp": "0070", "pressure": "001A",}
    {"rpm": "1D4E", "speed": "0080", "temp": "0080", "pressure": "001B",}
    {"rpm": "1E5F", "speed": "0090", "temp": "0090", "pressure": "001C",}
    {"rpm": "1F60", "speed": "0100", "temp": "0100", "pressure": "001D",}
]

data_cycle = cycle(test_data)  # Ensure the cycle is created outside the function

def get_test_data():
    test_refresh_rate = int(read_config('Test Parameters', 'TestRefreshRate'))
    while True:
        selected_data = next(data_cycle)
        print(f"Generated Test Data: {selected_data}")  # Debug output
        time.sleep(test_refresh_rate / 1000.0)
        yield selected_data
