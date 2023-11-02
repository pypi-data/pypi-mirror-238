
'''
import cyte.structs.DB.access as access
import cyte.structs.scan.regions.find_next as find_NEXT_REGION
NEXT_REGION = find_NEXT_REGION.START (
	access.DB ()
)
'''

def START (struct_DB):
	import cyte.structs.DB.access as access
	import cyte.structs.scan.struct.list as structs_LIST
	LIST = structs_LIST.find (struct_DB)
	
	LIST.sort (key = lambda struct : struct ["region"])
	
	LAST_INDEX = len (LIST) - 1;
	
	return LIST [ LAST_INDEX ][ "region" ] + 1
	
	