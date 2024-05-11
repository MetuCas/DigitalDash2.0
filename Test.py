# Test.py
import time
from config_utils import read_config
from itertools import cycle

# Updated test data to include 'voltage' and 'oil temp'
test_data = cycle([
    ["1A3F", "0050", "0050", "0018", "12F0", "005A"],
    ["1B2C", "0060", "0060", "0019", "12F1", "005B"],
    ["1C3D", "0070", "0070", "001A", "12F2", "005C"],
    ["1D4E", "0080", "0080", "001B", "12F3", "005D"],
    ["1E5F", "0090", "0090", "001C", "12F4", "005E"],
    ["1F60", "0100", "0100", "001D", "12F5", "005F"],
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
