#!/usr/bin/python3


def ADD_paths_TO_SYSTEM (paths):
	import pathlib
	FIELD = pathlib.Path (__file__).parent.resolve ()

	from os.path import dirname, join, normpath
	import sys
	for path in paths:
		sys.path.insert (0, normpath (join (FIELD, path)))



def CLIQUE ():
	import click
	@click.group ("keg")
	def GROUP ():
		pass

	'''
		./status_check keg OPEN \
		--port 10000
	'''
	@GROUP.command ("OPEN")
	@click.option ('--port', required = True)	
	@click.option ('--details', required = True)
	def OPEN (port, details):
		import json
		DETAILS = json.loads (details)
		module_paths = DETAILS ["module_paths"];
	
		ADD_paths_TO_SYSTEM (module_paths)
	
		from keg import TAP as TAP_keg
		
		TAP_keg (
			PORT = port
		)

		return;


	return GROUP
	
def START_CLICK ():
	import click
	@click.group ()
	def GROUP ():
		pass
		
	GROUP.add_command (CLIQUE ())
	GROUP ()

START_CLICK ()



#
