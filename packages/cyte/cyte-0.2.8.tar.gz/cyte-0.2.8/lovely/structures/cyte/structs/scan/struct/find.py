
'''
import cyte.structs.DB.access as access
import cyte.structs.scan.struct.find as find_struct
struct = find_struct.start (
	access.DB (),
	field = "region",
	value = 1
)	
'''

from tinydb import Query

def start (
	structs_DB,
	field,
	value
):
	Q = Query ()
	EL = structs_DB.get (
		Q [field] ==value
	)
	
	return