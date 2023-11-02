


'''
import cyte.structs.DB.access as access
import cyte.structs.scan.net as net_build
struct_net = net_build.start (access.DB ())
'''

'''
{
	"names": [
		"carbohydrates",
		"carbohydrate, by difference"
	],
	"region": 2,
	"includes": [ 7 ]
}
'''

import cyte.structs.DB.access as access
import cyte.structs.scan.struct.list as structs_LIST

import json

def find_included (struct_to_find, structs):
	#for struct in structs:
	#	if 

	return

def weave (struct_db):
	structs = structs_LIST.find (struct_db)
	structs_count = len (structs)

	print ("structs count:", structs_count)

	BRANCHES = []

	CYCLE_LIMIT = 20
	CYCLE = 1
	while (
		len (structs) >= 1 and
		CYCLE <= CYCLE_LIMIT
	):
		SELECTOR = 0
		LAST_INDEX = len (structs) - 1
		while (SELECTOR <= LAST_INDEX):
			struct = structs [ SELECTOR ]
		
			includes = struct ["includes"]
			
			if (len (includes) >= 1):
				print ('includes:', includes)
				
				included = find_included (struct, structs)
			
			
			
			SELECTOR += 1
		
		
		if (CYCLE == CYCLE_LIMIT):
			print ("cycle limit reached", len (structs), "of", structs_count)
	
		CYCLE += 1











