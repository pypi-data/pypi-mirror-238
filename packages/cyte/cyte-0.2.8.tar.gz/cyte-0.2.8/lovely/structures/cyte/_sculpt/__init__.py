

'''
	from os.path import dirname, join, normpath
	import sys
	import pathlib
	import cyte._sculpt as sculpt
	sculpt.start (
		normpath (join (
			pathlib.Path (__file__).parent.resolve (), "struct_2_multivitamin_276336.json"
		)),
		json.dumps (supplement_struct_2, indent = 4)
	)
'''
def start (path, string):
	f = open (path, "w")
	f.write	(string)
	f.close	()

	return;