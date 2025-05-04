import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from xj_telemetry_cluster import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Customize the dial to behave like an RPM gauge
        self.ui.rpm_dial.setMinimum(0)
        self.ui.rpm_dial.setMaximum(8000)  # Max RPM
        self.ui.rpm_dial.setNotchesVisible(True)
        self.ui.rpm_dial.setWrapping(False)
        self.ui.rpm_dial.setValue(0)

        # Connect signal to update the RPM label
        self.ui.rpm_dial.valueChanged.connect(self.update_rpm)

    def update_rpm(self, value):
        self.ui.rpm.setText(str(value))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
