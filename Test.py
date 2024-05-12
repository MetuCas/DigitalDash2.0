# Test.py created by Matthew Casinias and Jarred Javier
import time
from config_utils import read_config
from itertools import cycle

# Mimicking raw data output from Arduino
test_data = cycle([
    ["0x3E8", "0x0", "0x32", "0xC", "0x50", "0x78"],
    ["0x7D0", "0x14", "0x3C", "0xC", "0x51", "0x79"],
    ["0xDAC", "0x28", "0x46", "0xD", "0x52", "0x7A"],
    ["0x1770", "0x32", "0x50", "0xC", "0x53", "0x32"],
    ["0x1B58", "0x3C", "0x5A", "0xE", "0x0", "0x1F4"],
    ["0x1F40", "0x46", "0x64", "0xF", "0x8C", "0x208"],
])

def get_test_data():
    test_refresh_rate = int(read_config('Test Parameters', 'TestRefreshRate'))
    while True:
        selected_data = next(test_data)
        # Updated data dictionary to include new keys
        data = {
            'rpm': selected_data[0],
            'kph': selected_data[1],
            'wtr': selected_data[2],
            'bar': selected_data[3],
            'vlt': selected_data[4],
            'oil': selected_data[5] 
        }
        print(f"Generated Test Data: {data}")  # Debuging output
        time.sleep(test_refresh_rate / 1000.0)  # Convert ms to seconds
        yield data
