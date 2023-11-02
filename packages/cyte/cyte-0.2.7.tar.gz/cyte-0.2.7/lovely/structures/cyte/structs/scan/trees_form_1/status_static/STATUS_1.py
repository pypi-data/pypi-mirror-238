



'''
	python3 status/statuses/vitals/__init__.py "structs/scan/trees_form_1/status_static/STATUS_1.py"
'''

import cyte.structs.DB.access as access
import cyte.structs.scan.trees_form_1.printer as trees_form_1_printer

import json

def structs_db_path ():
	import pathlib
	from os.path import dirname, join, normpath
	return normpath (join (pathlib.Path (__file__).parent.resolve (), "structs.json"))

def check_1 ():
	struct_DB = access.DB (structs_db_path (), sort_keys = True)

	import cyte.structs.scan.trees_form_1 as trees_form_1
	trees = trees_form_1.start (struct_DB)
	trees_form_1_printer.write (trees)
	
	'''
	the_grove = ""
	def print_trees (trees, level):
		nonlocal the_grove;
	
		for tree in trees:
			names = tree ['names']
			indent = "  " * level
		
			print (f'{ indent }{ names }')
			the_grove += f'{ indent }{ str (names) }\n'
			
			if ("includes structs" in tree):
				print_trees (tree ["includes structs"], level = level + 1)
	
	print_trees (trees, level = 0)
	'''
	
	#print (json.dumps ({ "grove": trees }, indent = 4))
	

	import pathlib
	from os.path import dirname, join, normpath
	this_folder = str (pathlib.Path (__file__).parent.resolve ())
	with open (this_folder + '/the_grove.json') as f:	
		grove = json.load (f)["grove"]
		assert (grove == trees)
	
	#print (the_grove)

	
checks = {
	"CHECK 1": check_1
}