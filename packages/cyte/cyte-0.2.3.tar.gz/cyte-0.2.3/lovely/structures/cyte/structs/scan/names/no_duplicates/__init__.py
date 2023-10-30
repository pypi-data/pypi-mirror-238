
'''
raises an exception is a duplicate is found.
'''

'''
import cyte.structs.DB.access as access
from cyte.structs.scan.names.no_duplicates import structs_names_NO_DUPLICATES
structs_names_NO_DUPLICATES (
	access.DB ()
)
'''

import cyte.structs.scan as struct_scan

def structs_names_NO_DUPLICATES (
	structs_DB
):
	names = []

	def FOR_EACH (struct):
		struct_names = struct ["names"]
			
		for struct_name in struct_names:
			struct_name = struct_name.lower ()
		
			if (struct_name in names):
				raise Exception (f"duplicate found: { struct_name }")
		

	structs = struct_scan.START (
		FOR_EACH = FOR_EACH
	)

