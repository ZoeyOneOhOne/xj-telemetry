import obd
import time

connection = obd.OBD() 

timeout = 5
start_time = time.time()

while not connection.is_connected() and time.time() - start_time < timeout:
	print("Waiting for OBD2 adapter to connect...")
	time.sleep(1)
	
if connection.is_connected():
	print("OBD2 adapter connected.")

	def get_supported_pids(conn):
	        """Queries the vehicle for supported PIDs in the 01-20 range."""
	        if conn.is_connected():
	            response = conn.query(obd.commands.PIDS_A)
	            if not response.is_null():
	                supported_pids = []
	                bit_array = response.value
	                for i in range(20):
	                    if bit_array[i]:
	                        pid_hex = hex(i + 1)[2:].upper().zfill(2)
	                        supported_pids.append(f"PID 0x{pid_hex}")
	                return supported_pids
	            else:
	                return "Error: Could not retrieve supported PIDs."
	        else:
	            return "Error: Not connected to OBD-II adapter."
	
	supported_pids_01_20 = get_supported_pids(connection)
	print("Supported PIDs (01-20):", supported_pids_01_20)
else:
	print("Failed to connect to OBD2 adapter")
	exit()
	
commands =  {
	"RPM": obd.commands.RPM,
	"Speed": obd.commands.SPEED,
	"Throttle Position": obd.commands.THROTTLE_POS,
	"Intake Air Temp": obd.commands.INTAKE_TEMP,
	"Mass Air Flow": obd.commands.MAF,
	"Timing Advance": obd.commands.TIMING_ADVANCE,
	"Engine Load": obd.commands.ENGINE_LOAD
	}

try:
	while True:
		print("OBD2 Data")
		for name, command in commands.items():
			response = connection.query(command)
			if response.value is not None:
				print(f"{name}: {response.value}")
				with open("log.txt", "a") as f:
					f.write(f"{name}: {response.value}" + "\n")
			else:
				print(f"{name}: No Data")
				with open("log.txt", "a") as f:
					f.write(f"{name}: No Data" + "\n")
		time.sleep(1)
		
except KeyboardInterrupt:
	print("Exiting OBD2 reader")
	connection.close()
