import serial
from config_utils import read_config

def parse_data(line, key):
    settings = read_config('Serial Settings', key).split(',')
    byte_position = int(settings[0].strip().split(' ')[1]) - 1
    operation = settings[1].strip().split(' ')[0]
    operand = int(settings[1].strip().split(' ')[1])

    value = int(line[byte_position*3:(byte_position+1)*3], 16)  # Assumes byte data are spaced by a single space

    if operation == "Multiply":
        return value * operand
    elif operation == "Divide":
        return int(value / operand)  # Ensure division results are converted to int
    elif operation == "Add":
        return value + operand
    elif operation == "Subtract":
        return value - operand
    else:
        return value

def get_serial_data():
    ser = serial.Serial('COM3', timeout=1)  # Adjust to the correct COM port
    line = ser.readline().decode('utf-8').strip()
    rpm = parse_data(line, "RPM")
    speed = parse_data(line, "Speed")
    temperature = parse_data(line, "Temperature")
    pressure = parse_data(line, "Pressure")
    return {'rpm': rpm, 'speed': speed, 'temp': temperature, 'pressure': pressure}

def get_data():
    test_mode = read_config('Test Mode', 'Enabled').lower() == 'true'
    if test_mode:
        from Test import get_test_data
        return next(get_test_data())
    else:
        return get_serial_data()
