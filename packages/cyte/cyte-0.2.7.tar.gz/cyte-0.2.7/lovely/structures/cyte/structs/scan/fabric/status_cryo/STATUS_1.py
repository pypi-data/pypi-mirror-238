

'''
	python3 STATUS.py "structs/scan/net/status_cryo/STATUS_1.py"
'''

import cyte.structs.DB.access as access
import cyte.structs.scan.fabric as fabric

import json

def PATH ():
	import pathlib
	from os.path import dirname, join, normpath
	THIS_FOLDER = pathlib.Path (__file__).parent.resolve ()
	return normpath (join (THIS_FOLDER, "structs.json"))

def CHECK_1 ():
	struct_DB = access.DB (PATH (), sort_keys = True)
	#struct_DB = access.DB ()

	
	struct_fabric = fabric.weave (struct_DB)
	

	
	
checks = {
	"CHECK 1": CHECK_1
}