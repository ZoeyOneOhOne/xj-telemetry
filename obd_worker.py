from PyQt5.QtCore import QThread, pyqtSignal
import obd
import time
import logging

class OBDWorker(QThread):
    rpm_signal = pyqtSignal(float)
    engine_load_signal = pyqtSignal(float)
    intake_temp_signal = pyqtSignal(float)
    timing_advance_signal = pyqtSignal(float)
    print_signal = pyqtSignal(str)  # Signal for printing messages
    obd.logger.setLevel(logging.DEBUG)

    def __init__(self):
        super().__init__()
        self._running = True

    def run(self):
        print("Worker thread started.")
        try:
            connection = obd.OBD()
            self.print_signal.emit("OBD connection object created.")
        except Exception as e:
            self.print_signal.emit(f"Exception during OBD connection: {e}")
            return
        
        timeout = 5
        start_time = time.time()

        while not connection.is_connected() and time.time() - start_time < timeout:
            print("Waiting for OBD2 adapter to connect...")
            time.sleep(1)

        if not connection.is_connected():
            print("Failed to connect to OBD2 adapter")
            return

        print("OBD2 adapter connected.")

        commands = {
            "RPM": (obd.commands.RPM, self.rpm_signal),
            "Engine Load": (obd.commands.ENGINE_LOAD, self.engine_load_signal),
            "Intake Temp": (obd.commands.INTAKE_TEMP, self.intake_temp_signal),
            "Timing Advance": (obd.commands.TIMING_ADVANCE, self.timing_advance_signal),
        }

        while self._running:
            for name, (command, signal) in commands.items():
                response = connection.query(command)
                if not response.is_null():
                    value = response.value.magnitude if hasattr(response.value, 'magnitude') else float(response.value)
                    signal.emit(value)
            time.sleep(1)

    def stop(self):
        self._running = False
        self.quit()
        self.wait()
