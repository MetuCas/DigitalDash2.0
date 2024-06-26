#Created my Matthew Casinias
import serial
from config_utils import read_config
from Test import get_test_data

def parse_serial_data(line, key):
    settings = read_config('Serial Settings', key).split(',')
    byte_position = int(settings[0].split(' ')[1]) - 1
    operations = settings[1:]

    raw_value = int(line[byte_position*3:(byte_position+1)*3], 16)
    processed_value = apply_operations(raw_value, operations)
    return processed_value

def apply_operations(value, operations):
    for operation in operations:
        op, num = operation.strip().split(' ')
        num = int(num)
        if op == "Multiply":
            value *= num
        elif op == "Divide":
            value //= num
        elif op == "Add":
            value += num
        elif op == "Subtract":
            value -= num
    return value

def format_output(value):
    output_format = read_config('Output Settings', 'OutputFormat').strip()
    if output_format == 'Decimal':
        return str(value)
    elif output_format == 'Hexadecimal':
        return hex(value).upper().replace('0X', '')
    elif output_format == 'Binary':
        return bin(value)[2:]
    return str(value)

def get_serial_data():
    ser = serial.Serial('COM3', 9600, timeout=1)
    line = ser.readline().decode('utf-8').strip()
    data = {
        'rpm': parse_serial_data(line, "RPM"),
        'kph': parse_serial_data(line, "KPH"),
        'wtr': parse_serial_data(line, "WTR"),
        'bar': parse_serial_data(line, "BAR"),
        'vlt': parse_serial_data(line, "VLT"),
        'oil': parse_serial_data(line, "OIL")
    }
    return data

def process_data(data):
    # Process the data to a simple format without adding 'F'
    processed_data = {k: format_output(int(v, 16)) for k, v in data.items()}
    return processed_data

def get_data():
    test_mode = read_config('Test Mode', 'Enabled').lower() == 'true'
    if test_mode:
        data = next(get_test_data())
        print(f"Generated Test Data: {data}")  # Add this to see what's being generated
    else:
        data = get_serial_data()
    return process_data(data)

