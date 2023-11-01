

'''
import body_scan.functions.exceptions as bs_exceptions
'''

import io
import sys
import traceback
def find_trace (exception : Exception) -> str:
	try:
		file = io.StringIO ()
		traceback.print_exception (exception, file = file)
		
		#return traceback.format_stack()
		
		return file.getvalue ().rstrip ().split ("\n")
	except Exception:
		pass;
		
	return 'An exception occurred while calculating trace.'