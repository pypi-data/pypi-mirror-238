


'''
import cyte.structs.DB.access as access
import cyte.structs.sculpt.struct.insert as struct_INSERT
structs = struct_INSERT.START (
	access.DB (),
	{
		"names": [ '' ]
	}
)
'''

import cyte.structs.DB.access as access
import cyte.structs.scan.names.has as struct_has_name
import cyte.structs.scan.regions.find_next as find_next_region

def START (struct_db, struct):
	'''
		make sure that the struct doesn't already 
		exist in the db.
	'''
	names = struct ["names"]
	for name in names:
		found = struct_has_name.search (
			struct_db,
			name = name,
			return_bool = True
		)
		if (found == True):
			raise Exception (f"'{ name }' is already in the structs database.")



	#
	#
	#

	next_region = find_next_region.START (
		struct_db
	)
	
	struct ["region"] = next_region
	id = struct_db.insert (struct)
	assert (type (id) == int)

	return id