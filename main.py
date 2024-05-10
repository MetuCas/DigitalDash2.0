import socket
from Input import get_data
from config_utils import read_config
import time

def format_data(value, format):
    """Formats data based on the specified format."""
    if isinstance(value, str):
        value = int(value, 16)  # Convert hex string to integer if necessary
    if format == "Hexadecimal":
        return hex(value).upper().replace('0X', '')
    elif format == "Binary":
        return bin(value)[2:]
    elif format == "Decimal":
        return str(value)
    return value

def setup_server():
    """Sets up a server socket to accept a connection."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 9999))
    server_socket.listen(1)
    print("Server is waiting for a client to connect...")
    client_socket, _ = server_socket.accept()
    print("Client connected.")
    return client_socket

def main():
    client_socket = setup_server()
    refresh_rate = float(read_config('Output Settings', 'Refresh Rate'))  # Ensure this exists in your config.txt

    while True:
        data = get_data()  # Ensure this function correctly fetches the necessary data
        output_format = read_config('Output Settings', 'OutputFormat')  # Ensure this is correctly specified in config.txt
        formatted_data = {key: format_data(value, output_format) for key, value in data.items()}
        data_string = ','.join(f"{key}:{formatted_data[key]}" for key in formatted_data)
        client_socket.sendall(data_string.encode('utf-8'))
        time.sleep(refresh_rate)

    client_socket.close()

if __name__ == "__main__":
    main()
