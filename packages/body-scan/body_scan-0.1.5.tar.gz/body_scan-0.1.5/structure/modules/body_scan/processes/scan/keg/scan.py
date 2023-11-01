



def scan_file (path):
	with open (path, mode = 'r') as selector:
		return selector.read ()

def build_scan_string (path):
	contents = scan_file (path)
	contents += '''
		
try:
	______body_scan ["checks"] = checks;	
	______body_scan ["checks FOUND"] = True;
except Exception as E:
	print (E)
	______body_scan ["checks FOUND"] = False;
		'''

	return contents


import body_scan.functions.exceptions as bs_exceptions

import json
import time
from time import sleep, perf_counter as pc


def scan (FIND):
	# path = {}
	
	FINDINGS = []
	stats = {
		"passes": 0,
		"alarms": 0
	}

	path_E = ""

	try:
		CONTENTS = build_scan_string (FIND)
		
		______body_scan = {}
		exec (
			CONTENTS, 
			{ 
				'______body_scan': ______body_scan,
				'__file__': FIND
			}
		)
		

		if (______body_scan ["checks FOUND"] == False):
			return {
				"empty": True,
				"parsed": True
			}

		
		checks = ______body_scan ['checks']		

		
		for check in checks:
			try:
				TIME_START = pc ()
				checks [ check ] ()
				TIME_END = pc ()
				TIME_elapsed = TIME_END - TIME_START

				FINDINGS.append ({
					"check": check,
					"passed": True,
					"elapsed": [ TIME_elapsed, "SECONDS" ]
				})
				
				stats ["passes"] += 1
				
			except Exception as E:				
				FINDINGS.append ({
					"check": check,
					"passed": False,
					"exception": repr (E),
					"exception trace": bs_exceptions.find_trace (E)
				})
				
				stats ["alarms"] += 1
		
		
		return {
			"empty": False,
			"parsed": True,
						
			"stats": stats,			
			"checks": FINDINGS
		}
		
	except Exception as E:		
		path_E = E;

	return {
		"parsed": False,
		"alarm": "An exception occurred while scanning the path.",
		"exception": repr (path_E),
		"exception trace": bs_exceptions.find_trace (path_E)
	}