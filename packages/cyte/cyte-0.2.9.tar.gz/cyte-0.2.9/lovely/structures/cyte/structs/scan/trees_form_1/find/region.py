

'''
import cyte.structs.scan.trees_form_1.find.region as find_region
struct = find_region.start (region, trees_form_1_grove)
'''

import tinydb

def traverse (region, grove):
	for struct in grove:
		#print ("traversing struct:", struct ["names"])
	
		if (struct ['region'] == region):
			return struct;

		if (len (struct ["includes structs"]) >= 1):
			returns = traverse (region, struct ["includes structs"])
			print ("	returns:", type (returns))
			
			if (type (returns) == tinydb.table.Document):
				return returns;
				
	return False


def start (region, grove):
	returns = traverse (region, grove)
	if (returns == False):
		raise Exception (f"Region '{ region }' was not found.")
	
	return returns
	