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
				with open("truckLog.txt", "a") as f:
					f.write(f"{name}: {response.value}" + "\n")
			else:
				print(f"{name}: No Data")
				with open("truckLog.txt", "a") as f:
					f.write(f"{name}: No Data" + "\n")
		time.sleep(1)
		
except KeyboardInterrupt:
	print("Exiting OBD2 reader")
	connection.close()
