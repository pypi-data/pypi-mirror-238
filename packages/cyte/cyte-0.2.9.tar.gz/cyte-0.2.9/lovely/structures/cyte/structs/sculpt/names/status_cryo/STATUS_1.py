




'''
	python3 STATUS.py "structs/sculpt/names/status_cryo/STATUS_1.py"
'''


import cyte.structs.scan.regions.find_next as find_NEXT_REGION
import cyte.structs.sculpt.struct.insert as struct_INSERT
import cyte.structs.scan.struct.list as structs_LIST
	

def PATH (ADDRESS):
	import shutil

	import pathlib
	from os.path import dirname, join, normpath
	THIS_FOLDER = pathlib.Path (__file__).parent.resolve ()
	
	source = normpath (join (THIS_FOLDER, "structs.json"))
	DEST = normpath (join (THIS_FOLDER, ADDRESS))
	
	shutil.copyfile (source, DEST)
	
	return DEST;
	
def DELETE_PATH (ADDRESS):
	import pathlib
	from os.path import dirname, join, normpath
	THIS_FOLDER = pathlib.Path (__file__).parent.resolve ()
	DEST = normpath (join (THIS_FOLDER, ADDRESS))
	
	import os
	os.remove (DEST)

	return;

def CHECK_1 ():
	ADDRESS = "structs_1_1.JSON"

	try:
		DELETE_PATH (ADDRESS)
	except Exception as E:
		print (E)

	
	import cyte.structs.DB.access as access
	struct_DB = access.DB (PATH (ADDRESS))
	
	import cyte.structs.scan.names.has as struct_HAS_name
	struct = struct_HAS_name.search (
		struct_DB,
		name = "PROTEIN"
	)
	assert (len (struct ["names"]) == 1)
	assert (struct ["names"][0] == "protein")
		
	#
	#
	#
	
	import cyte.structs.sculpt.names as sculpt_names
	sculpt_names.START (
		struct_DB,
		REGION = 1,
		names = [ "protein", "proteina" ]
	)
	struct = struct_HAS_name.search (
		struct_DB,
		name = "PROTEIN"
	)
	
	print (struct)
	
	assert (len (struct ["names"]) == 2)
	assert (struct ["names"][0] == "protein")
	assert (struct ["names"][1] == "proteina")
	
	#
	#
	#
	

	DELETE_PATH (ADDRESS)

	return;
	
checks = {
	"CHECK 1": CHECK_1
}