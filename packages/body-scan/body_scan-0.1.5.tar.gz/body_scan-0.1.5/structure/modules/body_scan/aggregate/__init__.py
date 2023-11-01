
'''
	This function aggregates (or summarizes) the stats from
	all of the checks.
'''
def start (path_statusES):
	status = {
		"paths": path_statusES,
		"stats": {
			"alarms": 0,
			"empty": 0,
			"checks": {
				"passes": 0,
				"alarms": 0
			}
		}
	}
	
	for path in path_statusES:
		if ("empty" in path and path ["empty"] == True):
			status ["stats"] ["empty"] += 1
			continue;
		
		if ("alarm" in path):
			status ["stats"] ["alarms"] += 1
			continue;
		
		status ["stats"] ["checks"] ["passes"] += path ["stats"] ["passes"]
		status ["stats"] ["checks"] ["alarms"] += path ["stats"] ["alarms"]
		

	return status