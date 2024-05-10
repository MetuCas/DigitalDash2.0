import socket
import time
from Input import get_data
from config_utils import read_config

def format_data(value, format):
    """Formats data based on the specified format."""
    print(f"Formatting value: {value} with format: {format}")  # Debugging statement
    if isinstance(value, str):
        value = int(value, 16)  # Convert hex string to integer if necessary

    if "Hexadecimal" in format:
        formatted = hex(value).upper().replace('0X', '')
    elif "Binary" in format:
        formatted = bin(value)[2:]
    elif "Decimal" in format:
        formatted = str(value)
    else:
        formatted = str(value)  # Fallback if format isn't recognized
    print(f"Formatted output: {formatted}")  # More debugging
    return formatted

def setup_server():
    """Sets up a server socket to accept a connection."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 9999))
    server_socket.listen(1)
    print("Server is waiting for a client to connect...")
    client_socket, _ = server_socket.accept()
    print("Client connected.")
    return client_socket

def main():
    """Main function to process and send data continuously."""
    client_socket = setup_server()
    refresh_rate = float(read_config('Output Settings', 'Refresh Rate'))  # Read refresh rate from config

    try:
        while True:
            data = get_data()  # This function needs to be defined to fetch or generate data
            output_format = read_config('Output Settings', 'OutputFormat')
            formatted_data = {key: format_data(data[key], output_format) for key in data.keys()}
            data_string = ','.join(f"{key}:{formatted_data[key]}" for key in formatted_data)
            client_socket.sendall(data_string.encode('utf-8'))
            time.sleep(refresh_rate)  # Wait according to the refresh rate before sending the next data packet
    except KeyboardInterrupt:
        print("Server shutdown requested.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
