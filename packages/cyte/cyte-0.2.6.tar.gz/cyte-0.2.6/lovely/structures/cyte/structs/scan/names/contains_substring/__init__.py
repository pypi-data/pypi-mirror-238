
'''
	contains substring
'''

'''
import cyte.structs.DB.access as access
import cyte.structs.scan.names.contains_substring as structs_WHERE_name_CONTAINS_SUBSTRING
structs = structs_WHERE_name_CONTAINS_SUBSTRING.find (
	access.DB (),
	"VITAMIN B"
)
'''

import cyte.structs.scan as struct_scan

def find (
	structs_DB,
	CONTAINS
):
	CONTAINS = CONTAINS.upper ()

	def FOR_EACH (struct):
		struct_names = struct ["names"]
			
		for struct_name in struct_names:
			struct_name = struct_name.upper ()
		
			if (struct_name.__contains__ (CONTAINS)):
				#Q = Query ()
				#EL = db.get (Q.REGION == struct ["region"])
				
				return True

		return False
	
	structs = struct_scan.START (
		FOR_EACH = FOR_EACH
	)


	return structs