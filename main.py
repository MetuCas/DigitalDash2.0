import sys
import socket
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import QTimer
from Input import get_data
from config_utils import read_config

class DigitalCluster(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initTimer()
        self.setupServer()

    def setupServer(self):
        # Set up the server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 9999))  # Listen on localhost port 9999
        self.server_socket.listen(1)  # Listen for 1 connection
        self.client_socket, _ = self.server_socket.accept()  # Accept a connection

    def send_data(self, data):
        # Send data to the connected client
        try:
            self.client_socket.sendall(data.encode('utf-8'))
        except BrokenPipeError:
            print("Connection lost... attempting to reconnect.")
            self.client_socket, _ = self.server_socket.accept()

    def initUI(self):
        # Set up the user interface
        self.setWindowTitle("Vehicle Digital Cluster")
        layout = QVBoxLayout(self)
        self.rpm_label = QLabel("RPM: 0")
        self.speed_label = QLabel("Speed: 0 km/h")
        self.temp_label = QLabel("Engine Coolant Temp: 0°C")
        self.pressure_label = QLabel("Oil Pressure: 0 bar")
        layout.addWidget(self.rpm_label)
        layout.addWidget(self.speed_label)
        layout.addWidget(self.temp_label)
        layout.addWidget(self.pressure_label)
        self.setLayout(layout)

    def initTimer(self):
        # Set up a timer to periodically update the data
        refresh_rate = int(read_config('Input Settings', 'RefreshRate'))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateData)
        self.timer.start(refresh_rate)

    def updateData(self):
        # Fetch new data and update the UI
        output_format = read_config('Output Settings', 'OutputFormat').split('#')[0].strip()
        data = get_data()
        self.rpm_label.setText(f"RPM: {data['rpm']}")
        self.speed_label.setText(f"Speed: {data['speed']} km/h")
        self.temp_label.setText(f"Engine Coolant Temp: {data['temp']}°C")
        self.pressure_label.setText(f"Oil Pressure: {data['pressure']} bar")
        data_string = f"{data['rpm']}, {data['speed']}, {data['temp']}, {data['pressure']}"
        self.send_data(data_string)

    def closeEvent(self, event):
        # Clean up sockets when closing the application
        self.client_socket.close()
        self.server_socket.close()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = DigitalCluster()
    ex.show()
    sys.exit(app.exec())
