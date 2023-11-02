
'''
	python3 STATUS.py "structs/scan/names/no_duplicates/STATUS_DYNAMIC_1.py"
'''

def CHECK_1 ():
	import cyte.structs.DB.access as access
	from cyte.structs.scan.names.no_duplicates import structs_names_NO_DUPLICATES
	structs_names_NO_DUPLICATES (
		access.DB ()
	)
	
checks = {
	"dynamic, no duplicates found": CHECK_1
}