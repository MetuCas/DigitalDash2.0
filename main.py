# main.py
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import QTimer
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
        refresh_rate = int(read_config('Input Settings', 'RefreshRate'))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateData)
        self.timer.start(refresh_rate)

    def updateData(self):
        output_format = read_config('Output Settings', 'OutputFormat').split('#')[0].strip()  # Strip out comments and whitespace
        print("Output Format:", output_format)  # Debugging print statement
        data = get_data()
        self.rpm_label.setText(f"RPM: {format_data(data['rpm'], output_format)}")
        self.speed_label.setText(f"Speed: {format_data(data['speed'], output_format)} km/h")
        self.temp_label.setText(f"Engine Coolant Temp: {format_data(data['temp'], output_format)}°C")
        self.pressure_label.setText(f"Oil Pressure: {format_data(data['pressure'], output_format)} bar")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = DigitalCluster()
    ex.show()
    sys.exit(app.exec())
