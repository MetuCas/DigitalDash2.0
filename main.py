import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer
from Input import get_data
from config_utils import read_config

class DigitalCluster(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initTimer()

    def initUI(self):
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
        refresh_rate = int(read_config('Input Settings', 'RefreshRate'))  # Correctly using read_config
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateData)
        self.timer.start(refresh_rate)

    def updateData(self):
        data = get_data()
        self.rpm_label.setText(f"RPM: {data['rpmF']}")
        self.speed_label.setText(f"Speed: {data['speedF']} km/h")
        self.temp_label.setText(f"Engine Coolant Temp: {data['tempF']}°C")
        self.pressure_label.setText(f"Oil Pressure: {data['pressureF']} bar")

def run_application():
    app = QApplication(sys.argv)
    ex = DigitalCluster()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    if os.getenv('DISPLAY', '') == '':
        print('No display found. Using :0.0.')
        os.environ.__setitem__('DISPLAY', ':0.0')
    run_application()
