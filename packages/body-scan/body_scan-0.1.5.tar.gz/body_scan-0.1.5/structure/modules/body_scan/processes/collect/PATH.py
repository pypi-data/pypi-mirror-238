



'''
	import body_scan.PROCESSES.COLLECT.path as COLLECT_path
	COLLECT_path.FIND ()
'''
import pathlib
from os.path import dirname, join, normpath

def FIND ():
	return normpath (join (pathlib.Path (__file__).parent.resolve (), "START.PROC.PY"))