from PyQt5.QtWidgets import QApplication, QMainWindow
from xj_telemetry_cluster import Ui_MainWindow
from obd_worker import OBDWorker  # Import your worker class
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.worker = OBDWorker()

        # Connect signals from the worker to the GUI
        self.worker.rpm_signal.connect(self.ui.rpm_dial.setValue)
        self.worker.engine_load_signal.connect(self.ui.engine_load_dial.setValue)
        self.worker.intake_temp_signal.connect(self.ui.intake_temp_dial.setValue)
        self.worker.timing_advance_signal.connect(self.ui.timing_advance_dial.setValue)
        self.worker.print_signal.connect(print)  # Route worker print messages to the terminal

        # Start the thread
        self.worker.start()

        # Set a custom style sheet to make the dial look cooler
        self.ui.rpm_dial.setStyleSheet("""
            QDial {
                background-color: #222;
            }
            QDial::groove {
                background: #444;
            }
            QDial::handle {
                background: red;
                width: 5px;
            }
        """)

        # RPM gauge
        self.ui.rpm_dial.setMinimum(0)
        self.ui.rpm_dial.setMaximum(6000)
        self.ui.rpm_dial.setNotchesVisible(True)
        self.ui.rpm_dial.setSingleStep(5) 
        self.ui.rpm_dial.setPageStep(100)
        self.ui.rpm_dial.setWrapping(False)
        self.ui.rpm_dial.setValue(0)

        # RPM label
        self.ui.rpm_dial.valueChanged.connect(self.update_rpm)

        # Engine load gauge
        self.ui.engine_load_dial.setMinimum(0)
        self.ui.engine_load_dial.setMaximum(100)
        self.ui.engine_load_dial.setNotchesVisible(True)
        self.ui.engine_load_dial.setSingleStep(1)
        self.ui.engine_load_dial.setPageStep(10)
        self.ui.engine_load_dial.setWrapping(False)
        self.ui.engine_load_dial.setValue(0)

        # Engine load label
        self.ui.engine_load_dial.valueChanged.connect(self.update_engine_load)

        # Intake Temp gauge
        self.ui.intake_temp_dial.setMinimum(0)
        self.ui.intake_temp_dial.setMaximum(120)
        self.ui.intake_temp_dial.setNotchesVisible(True)
        self.ui.intake_temp_dial.setSingleStep(1)
        self.ui.intake_temp_dial.setPageStep(10)
        self.ui.intake_temp_dial.setWrapping(False)
        self.ui.intake_temp_dial.setValue(0)

        # Intake Temp label
        self.ui.intake_temp_dial.valueChanged.connect(self.update_intake_temp)

        # Timing advance gauge
        self.ui.timing_advance_dial.setMinimum(0)
        self.ui.timing_advance_dial.setMaximum(50)
        self.ui.timing_advance_dial.setNotchesVisible(True)
        self.ui.timing_advance_dial.setSingleStep(1)
        self.ui.timing_advance_dial.setPageStep(5)
        self.ui.timing_advance_dial.setWrapping(False)
        self.ui.timing_advance_dial.setValue(0)

        # Timing advance label
        self.ui.timing_advance_dial.valueChanged.connect(self.update_timing_advance)

    def update_rpm(self, value):
        self.ui.rpm.setText(str(value))

    def update_engine_load(self, value):
        self.ui.engine_load.setText(str(value))

    def update_intake_temp(self, value):
        self.ui.intake_temp.setText(str(value))

    def update_timing_advance(self, value):
        self.ui.timing_advance.setText(str(value))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
