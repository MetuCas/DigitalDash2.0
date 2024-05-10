import sys
import socket
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer, Qt
from Input import get_data
from config_utils import read_config

class DigitalCluster(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initTimer()
        self.setupServer()

    def setupServer(self):
        print("Creating server socket...")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('localhost', 9999))
        self.server_socket.listen(1)
        self.client_socket, _ = self.server_socket.accept()
        print("Client connected.")

    def send_data(self, data):
        try:
            self.client_socket.sendall(data.encode('utf-8'))
            print("Data sent:", data)
        except BrokenPipeError:
            print("Connection lost... attempting to reconnect.")
            self.client_socket, _ = self.server_socket.accept()

    def initUI(self):
        self.setWindowTitle("Vehicle Digital Cluster")
        self.setGeometry(100, 100, 480, 320)
        layout = QVBoxLayout(self)
        self.rpm_label = QLabel("RPM: 0", self)
        self.speed_label = QLabel("Speed: 0 km/h", self)
        self.temp_label = QLabel("Engine Coolant Temp: 0°C", self)
        self.pressure_label = QLabel("Oil Pressure: 0 bar", self)

        labels = [self.rpm_label, self.speed_label, self.temp_label, self.pressure_label]
        for label in labels:
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)

        self.setLayout(layout)

    def initTimer(self):
        refresh_rate = int(read_config('Input Settings', 'RefreshRate'))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateData)
        self.timer.start(refresh_rate)

    def updateData(self):
        data = get_data()
        self.rpm_label.setText(f"RPM: {data['rpm']}")
        self.speed_label.setText(f"Speed: {data['speed']} km/h")
        self.temp_label.setText(f"Engine Coolant Temp: {data['temp']}°C")
        self.pressure_label.setText(f"Oil Pressure: {data['pressure']} bar")
        data_string = f"{data['rpm']}, {data['speed']}, {data['temp']}, {data['pressure']}"
        self.send_data(data_string)

    def closeEvent(self, event):
        self.client_socket.close()
        self.server_socket.close()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = DigitalCluster()
    ex.show()
    sys.exit(app.exec_())
