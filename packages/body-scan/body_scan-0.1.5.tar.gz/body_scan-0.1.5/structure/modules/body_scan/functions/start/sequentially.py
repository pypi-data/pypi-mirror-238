


'''
	starts checks one after another, sequentially
'''

import body_scan.processes.scan as scan

def now (
	finds,
	module_paths,
	relative_path,
	records
):
	path_statuses = []
	for path in finds:	
		[ status ] = scan.start (		
			path = path,
			module_paths = module_paths,
			relative_path = relative_path,
			records = records
		)
		
		path_statuses.append (status)
		
	return path_statuses;