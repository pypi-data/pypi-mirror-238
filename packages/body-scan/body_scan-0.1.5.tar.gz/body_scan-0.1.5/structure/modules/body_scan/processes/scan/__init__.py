

'''
	This is the scan process starter.
'''

'''
	steps:
		1. 	A scan process is started.
			1. the scan process has a flask (a.k.a. keg or reservoir) server built in.
		
		2. 	A request is sent to the scan process to run checks found
			in a path.
		
		3. 	The returns (status and stats) of the scan process are returned.
'''

from BOTANIST.PORTS.FIND_AN_OPEN_PORT import FIND_AN_OPEN_PORT
from BOTANIST.PROCESSES.START_MULTIPLE import START_MULTIPLE as START_MULTIPLE_PROCESSES

import body_scan.processes.scan.path as SCAN_path
	
import sys
import json
def ATTEMPT_TAP_keg (
	module_paths
):
	PORT = FIND_AN_OPEN_PORT ()
	SCAN_PROCESS_path = SCAN_path.FIND ()

	details = json.dumps ({ "module_paths": sys.path })
	string = f'''python3 { SCAN_PROCESS_path } keg OPEN --port { PORT } --details \'{ details }\' '''

	PROCS = START_MULTIPLE_PROCESSES (
		PROCESSES = [{
			"STRING": string,
			"CWD": None
		}]
	)

	return [ PORT, PROCS ]

def start (
	path,
	module_paths = [],
	relative_path = False,
	records = 0
):
	[ PORT, PROCS ] = ATTEMPT_TAP_keg (
		module_paths
	)
	
	import time
	time.sleep (0.5)
	
	REQUEST_ADDRESS = f'http://127.0.0.1:{ PORT }'
	
	import json
	import requests
	r = requests.put (
		REQUEST_ADDRESS, 
		data = json.dumps ({ 
			"FINDS": [ str (path) ],
			"MODULE paths": module_paths,
			"RELATIVE path": relative_path
		})
	)
	
	def format_response (TEXT):
		import json
		return json.loads (TEXT)
	
	status = format_response (r.text)

	if (records >= 2):
		print ()
		print ("request address:", REQUEST_ADDRESS)
		print ("request status:", r.status_code)
		print ("request text:", json.dumps (status, indent = 4))
		print ()


	EXIT 			= PROCS ["EXIT"]
	PROCESSES 		= PROCS ["PROCESSES"]
	
	return [ status ]