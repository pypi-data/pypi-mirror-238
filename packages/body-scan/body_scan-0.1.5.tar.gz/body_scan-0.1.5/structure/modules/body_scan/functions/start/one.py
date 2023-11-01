


'''
'''

import body_scan.processes.scan as scan

def now (
	before,
	module_paths,
	relative_path,
	records
):
	[ status ] = scan.start (		
		path = before,
		module_paths = module_paths,
		relative_path = relative_path,
		records = records
	)
		
	return status;