


'''

INCLUDES = "VITAMIN B"

def FOR_EACH (struct):
	struct_names = struct ["names"]
		
	for struct_name in struct_names:
		struct_name = struct_name.upper ()
	
		if (struct_name.__contains__ (INCLUDES)):
			#Q = Query ()
			#EL = db.get (Q.REGION == struct ["region"])
			
			return True

	return True

import cyte.structs.DB.access as access
import cyte.structs.scan as struct_scan
structs = struct_scan.START (
	structs_DB = access.DB (),
	FOR_EACH = FOR_EACH
)
'''

from tinydb import TinyDB, Query
import cyte.structs.DB.PATH as structs_DB_PATH

def START (
	structs_DB = None,
	FOR_EACH = lambda : ()
):
	PATH = structs_DB_PATH.find ()

	db = TinyDB (PATH)
	LIST = db.all ()
	
	RETURNS = []
	
	for struct in LIST:		
		if (FOR_EACH (struct) == True):
			RETURNS.append (struct)
				
	return RETURNS
	