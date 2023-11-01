
'''
	import pathlib
	from os.path import dirname, join, normpath
	
	this_folder = pathlib.Path (__file__).parent.resolve ()
	search = normpath (join (this_folder, "../.."))

	import body_scan
	body_scan.start (
		glob_string = search + '/**/*status.py'
	)
'''

import glob
import json

import body_scan.aggregate as aggregate
import body_scan.processes.scan as scan

import body_scan.functions.alarm_printer as alarm_printer
import body_scan.functions.start.sequentially as start_sequentially
import body_scan.functions.start.simultaneously as start_simultaneously
import body_scan.functions.start.one as start_one

from tinydb import TinyDB, Query

'''
	
'''
def start (
	glob_string = "",
	relative_path = False,
	module_paths = [],
	simultaneous = False,
	print_alarms = True,
	records = 1,
	db_directory = False,
	
	before = False,
	after = False
):
	finds = glob.glob (glob_string, recursive = True)
		
	relative_path = str (relative_path)	
		
	if (records >= 2):
		print ()
		print ("searching for glob_string:")
		print ("	", glob_string)
		print ()
	
	if (records >= 2):
		print ()
		print ("	finds:", finds)
		print ("	finds count:", len (finds))
		print ();

	if (type (before) == str):
		before_path_statuses = start_one.now (
			before,
			module_paths,
			relative_path,
			records
		)
		print ("before path statuses:", json.dumps (before_path_statuses, indent = 4))
		
		assert (before_path_statuses ['stats']['passes'] >= 1)
		assert (before_path_statuses ['stats']['alarms'] == 0)
		

	if (simultaneous == True):
		path_statuses = start_simultaneously.now (
			finds,
			module_paths,
			relative_path,
			records
		)
	else:
		path_statuses = start_sequentially.now (
			finds,
			module_paths,
			relative_path,
			records
		)
		
	if (type (after) == str):
		after_path_statuses = start_one.now (
			after,
			module_paths,
			relative_path,
			records
		)
		print ("before path statuses:", json.dumps (after_path_statuses, indent = 4))
		
		assert (after_path_statuses ['stats']['passes'] >= 1)
		assert (after_path_statuses ['stats']['alarms'] == 0)

	status = aggregate.start (
		path_statuses
	)

	'''
		status
		alarms
		stats
	'''
	alarms = alarm_printer.start (status ["paths"])
	stats = status ["stats"]
	paths = status ["paths"]
	
	if (records >= 1):
		print ("paths:", json.dumps (paths, indent = 4))
		print ("alarms:", json.dumps (alarms, indent = 4))
		print ("stats:", json.dumps (stats, indent = 4))	
		
	if (type (db_directory) == str):
		import pathlib
		from os.path import dirname, join, normpath
		db_file = normpath (join (db_directory, f"records.json"))
		db = TinyDB (db_file)
		
		db.insert ({
			'paths': paths, 
			'alarms': alarms,
			'stats': stats
		})
		
		db.close ()
		
		
	return {
		"status": status,
		
		"paths": paths,
		"alarms": alarms,
		"stats": stats
	}
	
