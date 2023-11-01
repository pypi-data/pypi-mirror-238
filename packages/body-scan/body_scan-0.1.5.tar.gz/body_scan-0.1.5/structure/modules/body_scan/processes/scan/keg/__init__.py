

def ADD_paths_TO_SYSTEM (paths):
	import pathlib
	FIELD = pathlib.Path (__file__).parent.resolve ()

	from os.path import dirname, join, normpath
	import sys
	for path in paths:
		sys.path.insert (0, normpath (join (FIELD, path)))

from .scan import scan

import json

def TAP (
	PORT = 0,
	records = 0
):
	if (records >= 1):
		print ("opening scan process keg on port:", PORT)

	from flask import Flask, request

	app = Flask (__name__)

	@app.route ("/", methods = [ 'GET' ])
	def HOME ():	
		return "?"

	@app.route ("/", methods = [ 'PUT' ])
	def HOME_POST ():
		if (records >= 1):
			print ("@ HOME PUT", request.data)
	
		DATA = json.loads (request.data.decode ('utf8'))
		
		if (records >= 1):
			print ("DATA:", DATA)

		FINDS = DATA ['FINDS']
		module_paths = DATA ['MODULE paths']
		relative_path = DATA ['RELATIVE path']

		ADD_paths_TO_SYSTEM (module_paths)

		status = {
			"paths": [],
			"stats": {
				"empty": 0,
				"checks": {
					"passes": 0,
					"alarms": 0
				}
			}
		}
		
		status = {}

		for FIND in FINDS:
			SCAN_status = scan (FIND)
			
			import os
			if (type (relative_path) == str):
				path = os.path.relpath (FIND, relative_path)
			else:
				path = FIND
			
			
			status = {
				"path": path,
				** SCAN_status
			};
			
			
		return json.dumps (status, indent = 4)
		
	app.run (
		'0.0.0.0',
		port = PORT,
		debug = False
	)