

'''
	????
		possibly this is the tree with replications
		of structures.
		
			protein is in multiple places:
		
				strength
					protein
					
				energy
					protein
					carbs
					lipids
					
			afterwards, grove can be scanned again to reduce the
			grove to a list?
			
			when building the grove, 			
			
'''

import cyte.structs.DB.access as access
import cyte.structs.scan.struct.list as structs_LIST

import json


'''
class grow:
	pass;
'''
	

def start (struct_DB):
	structs = structs_LIST.find (struct_DB)
	structs_tally = len (structs)

	#
	#	this is a list of all the struct regions that have 
	#
	#	{
	#		1: 2	
	#	}
	#
	#	
	struct_region_tallies = {}

	def find_region (region):
		for struct in structs:
			if (struct ['region'] == region):
				return struct;
				
		raise Exception (f"'region' '{ region }' was not found in structs.")


	def build_tree (region):
		struct = find_region (region)
		struct ["includes structs"] = []
		
		includes = struct ["includes"]		
		for include in includes:
			struct ["includes structs"].append (build_tree (include))
		
		return struct;

	print ("structs tally:", structs_tally)

	

	trees = []


	selector = 0
	last_index = len (structs) - 1
	while (selector <= last_index):
		struct = structs [ selector ]
		
		struct ["includes structs"] = []
		includes = struct ["includes"]		
		for include in includes:
			struct ["includes structs"].append (build_tree (include))

		trees.append (struct)
		
		selector += 1
		
		
	return trees;
	
