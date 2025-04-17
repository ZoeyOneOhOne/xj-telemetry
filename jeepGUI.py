import sys
import time
import threading
import obd

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QGridLayout
)
from PyQt5.QtCore import QTimer

class OBD2Monitor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jeep OBD2 Monitor")
        self.resize(400, 300)

        # Create layout and labels
        self.layout = QVBoxLayout()
        self.grid = QGridLayout()
        self.labels = {}

        self.commands = {
            "RPM": obd.commands.RPM,
            "Speed": obd.commands.SPEED,
            "Throttle Position": obd.commands.THROTTLE_POS,
            "Intake Air Temp": obd.commands.INTAKE_TEMP,
            "Mass Air Flow": obd.commands.MAF,
            "Timing Advance": obd.commands.TIMING_ADVANCE,
            "Engine Load": obd.commands.ENGINE_LOAD
        }

        # Create label widgets for each command
        row = 0
        for name in self.commands:
            label = QLabel(f"{name}: Waiting...")
            self.labels[name] = label
            self.grid.addWidget(label, row, 0)
            row += 1

        self.layout.addLayout(self.grid)
        self.setLayout(self.layout)

        # Start OBD2 connection in a separate thread
        self.connection = None
        threading.Thread(target=self.connect_obd2, daemon=True).start()

        # Update every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)

    def connect_obd2(self):
        self.connection = obd.OBD()
        timeout = 5
        start_time = time.time()

        while not self.connection.is_connected() and time.time() - start_time < timeout:
            print("Waiting for OBD2 adapter to connect...")
            time.sleep(1)

        if self.connection.is_connected():
            print("OBD2 adapter connected.")
        else:
            print("Failed to connect to OBD2 adapter")
            self.connection = None

    def update_data(self):
        if not self.connection or not self.connection.is_connected():
            for name in self.labels:
                self.labels[name].setText(f"{name}: Not connected")
            return

        for name, command in self.commands.items():
            response = self.connection.query(command)
            if response and response.value is not None:
                self.labels[name].setText(f"{name}: {response.value}")
            else:
                self.labels[name].setText(f"{name}: No Data")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OBD2Monitor()
    window.show()
    sys.exit(app.exec_())
