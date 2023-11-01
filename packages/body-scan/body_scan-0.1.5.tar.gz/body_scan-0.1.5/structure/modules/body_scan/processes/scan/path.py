
'''
	import body_scan.PROCESSES.SCAN.path as SCAN_path
	SCAN_path.FIND ()
'''
'''
	This returns the path of the "scan" process.
'''


import pathlib
from os.path import dirname, join, normpath

path = "scan.process.py"

def FIND ():
	this_folder = pathlib.Path (__file__).parent.resolve ()
	return normpath (join (this_folder, path))