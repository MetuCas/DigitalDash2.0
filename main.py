import sys
import socket
from Input import get_data
from config_utils import read_config

def format_data(value, format):
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
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 9999))
    server_socket.listen(1)
    print("Server is waiting for a client to connect...")
    return server_socket

def main():
    server_socket = setup_server()
    client_socket, addr = server_socket.accept()
    print(f"Client connected from {addr}")

    while True:
        try:
            data = get_data()  # Fetch data from your sensors or internal logic
            formatted_data = {key: format_data(value, 'Decimal') for key, value in data.items()}
            data_string = ','.join(f"{key}:{value}" for key, value in formatted_data.items())
            client_socket.sendall(data_string.encode('utf-8'))
        except (BrokenPipeError, ConnectionResetError):
            print("Connection lost... trying to reconnect.")
            client_socket, addr = server_socket.accept()
            print(f"Client reconnected from {addr}")
        except KeyboardInterrupt:
            print("Server is shutting down.")
            break

    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()
