# Test.py
import time
from config_utils import read_config
from itertools import cycle

# Updated test data to include 'voltage' and 'oil temp'
test_data = cycle([
    ["1000", "0000", "0050", "0012", "0080", "0120"],
    ["2000", "0020", "0060", "0012", "0081", "0121"],
    ["3500", "0040", "0070", "0013", "0082", "0122"],
    ["6000", "0050", "0080", "0012", "0083", "0050"],
    ["7000", "0060", "0090", "0014", "0000", "0500"],
    ["8000", "0070", "0100", "0015", "0140", "0520"],
])

def get_test_data():
    test_refresh_rate = int(read_config('Test Parameters', 'TestRefreshRate'))
    while True:
        selected_data = next(test_data)
        # Updated data dictionary to include new keys
        data = {
            'rpm': selected_data[0],
            'speed': selected_data[1],
            'temp': selected_data[2],
            'pressure': selected_data[3],
            'voltage': selected_data[4],  # New
            'oil_temp': selected_data[5]  # New
        }
        print(f"Generated Test Data: {data}")  # Debug output
        time.sleep(test_refresh_rate / 1000.0)  # Convert ms to seconds
        yield data
