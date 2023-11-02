



'''
	python3 STATUS.py "structs/scan/names/has/STATUS_dynamic_1.py"
'''



def CHECK_1 ():
	import cyte.structs.DB.access as access
	import cyte.structs.scan.names.has as struct_HAS_name
	struct = struct_HAS_name.search (
		access.DB (),
		name = "PROTEIN"
	)
	
	print (struct)

	import tinydb
	assert (type (struct) == tinydb.table.Document)
	assert (struct ["region"] == 1)
	
	
checks = {
	"dynamic, has name": CHECK_1
}