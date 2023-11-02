



'''
	python3 STATUS.py "structs/scan/names/has/STATUS_static_1.py"
'''

def PATH ():
	import pathlib
	from os.path import dirname, join, normpath
	THIS_FOLDER = pathlib.Path (__file__).parent.resolve ()
	return normpath (join (THIS_FOLDER, "structs.json"))

def CHECK_1 ():
	import cyte.structs.DB.access as access
	import cyte.structs.scan.names.has as struct_HAS_name
	FOUND = struct_HAS_name.search (
		access.DB (PATH ()),
		name = "PROTEIN",
		return_bool = True
	)

	assert (FOUND == True)
	
def CHECK_2 ():
	import cyte.structs.DB.access as access
	import cyte.structs.scan.names.has as struct_HAS_name
	FOUND = struct_HAS_name.search (
		access.DB (PATH ()),
		name = "PROTEINN",
		return_bool = True
	)

	assert (FOUND == False)
	
	
checks = {
	"static, has name 1": CHECK_1,
	"static, has name 2": CHECK_2
}