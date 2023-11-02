

'''
python3 STATUS.py "structs/scan/_STATUS/STATUS_dynamic_1.py"
'''


def CHECK_1 ():
	INCLUDES = "VITAMIN B1"

	def FOR_EACH (struct):
		struct_names = struct ["names"]
			
		for struct_name in struct_names:
			struct_name = struct_name.upper ()
		
			if (struct_name == INCLUDES.upper ()):
				return True

		return False

	import cyte.structs.DB.access as access
	import cyte.structs.scan as struct_scan
	structs = struct_scan.START (
		structs_DB = access.DB (),
		FOR_EACH = FOR_EACH
	)
	
	print ("structs:", structs)

	return;
	
	
checks = {
	"check 1": CHECK_1
}