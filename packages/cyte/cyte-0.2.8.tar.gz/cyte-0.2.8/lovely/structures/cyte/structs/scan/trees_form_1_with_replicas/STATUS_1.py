



'''
	python3 status.py "structs/scan/trees_form_1_with_replicas/STATUS_1.py"
'''

import cyte.structs.DB.access as access
import cyte.structs.scan.trees_form_1_with_replicas as trees_form_1_with_replicas

import json

def PATH ():
	import pathlib
	from os.path import dirname, join, normpath
	THIS_FOLDER = pathlib.Path (__file__).parent.resolve ()
	return normpath (join (THIS_FOLDER, "structs.json"))

def CHECK_1 ():
	#struct_DB = access.DB (PATH (), sort_keys = True)
	struct_DB = access.DB ()

	
	trees = trees_form_1_with_replicas.start (struct_DB)
	
	import json
	print (json.dumps (trees, indent = 4))
	
	def print_trees (trees, level):
		for tree in trees:
			names = tree ['names']
			indent = "  " * level
		
			print (f'{ indent }{ names }')
			
			if ("includes structs" in tree):
				print_trees (tree ["includes structs"], level = level + 1)
	
	print_trees (trees, level = 0)
	
checks = {
	"CHECK 1": CHECK_1
}