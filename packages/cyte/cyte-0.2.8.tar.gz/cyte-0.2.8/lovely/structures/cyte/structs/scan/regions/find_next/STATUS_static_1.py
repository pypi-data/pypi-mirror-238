

'''
	python3 STATUS.py "structs/scan/regions/find_next/STATUS_dynamic_1.py"
'''

import cyte.structs.DB.access as access
import cyte.structs.scan.regions.find_next as find_NEXT_REGION

def PATH ():
	import pathlib
	from os.path import dirname, join, normpath
	THIS_FOLDER = pathlib.Path (__file__).parent.resolve ()
	return normpath (join (THIS_FOLDER, "structs.json"))

def CHECK_1 ():
	NEXT_REGION = find_NEXT_REGION.START (
		access.DB (PATH ())
	)
	
	assert (NEXT_REGION == 53), NEXT_REGION

	return;
	
checks = {
	"CHECK 1": CHECK_1
}