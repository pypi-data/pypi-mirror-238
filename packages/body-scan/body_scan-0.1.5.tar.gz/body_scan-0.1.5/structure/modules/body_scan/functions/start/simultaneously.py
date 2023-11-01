

import body_scan.processes.scan as scan

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def now (
	finds,
	module_paths,
	relative_path,
	records
):
	OUTPUT = []

	def FN (path):
		[ status ] = scan.start (		
			path = path,
			module_paths = module_paths,
			relative_path = relative_path,
			records = records
		)
	
		return status;
	
	
	with ThreadPoolExecutor () as executor:
		RETURNS = executor.map (
			FN, 
			finds
		)
		
		executor.shutdown (wait = True)
		
		for RETURN in RETURNS:
			OUTPUT.append (RETURN)
			
		
	return OUTPUT;