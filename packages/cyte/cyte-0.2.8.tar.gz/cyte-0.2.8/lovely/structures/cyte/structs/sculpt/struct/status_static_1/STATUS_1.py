




'''
	python3 STATUS.py "structs/sculpt/struct/STATUS_STATIC_1/STATUS_1.py"
'''

import cyte.structs.DB.access as access
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
	

	struct_DB = access.DB (PATH (ADDRESS))

	NEXT_REGION = find_NEXT_REGION.START (struct_DB)
	assert (NEXT_REGION == 53), NEXT_REGION
	LIST = structs_LIST.find (struct_DB)
	assert (len (LIST) == 52), len (LIST)
	
	
	struct_INSERT.START (
		struct_DB,
		{
			'PART OF': [], 
			"names": [ 'EXAMPLE struct' ]
		}
	)
	
	NEXT_REGION = find_NEXT_REGION.START (struct_DB)
	assert (NEXT_REGION == 54), NEXT_REGION
	
	LIST = structs_LIST.find (struct_DB, SORT = "region")
	#print (LIST)
	assert (len (LIST) == 53), len (LIST)
	
	DELETE_PATH (ADDRESS)

	return;
	
checks = {
	"CHECK 1": CHECK_1
}