


'''
#
#	tries to return the struct with the name provided.
#
#	raises an exception is "protein" is not found.
#
import cyte.structs.DB.access as access
import cyte.structs.scan.names.has as struct_has_name
struct = struct_has_name.search (
	access.DB (),
	name = "protein"
)
'''

'''
#
#	returns True if "protein" is found, otherwise returns False
#
import cyte.structs.DB.access as access
import cyte.structs.scan.names.has as struct_has_name
found = struct_has_name.search (
	access.DB (),
	name = "protein",
	return_bool = True
)
'''

from tinydb import TinyDB, Query
import cyte.structs.DB.PATH as structs_DB_PATH

def search (
	structs_db,
	name = "",
	
	return_bool = False
):
	LIST = structs_db.all ()
	
	name = name.lower ()
	
	for struct in LIST:
		struct_names = struct ["names"]
		
		for struct_name in struct_names:
			if (name == struct_name.lower ()):			
				Q = Query ()
				EL = structs_db.get (Q.region == struct ["region"])
				
				if (return_bool == True):
					return True
				else:
					return EL
				
				
	if (return_bool == True):
		return False
		
	raise Exception (f'name "{ name }" was not found.')
	