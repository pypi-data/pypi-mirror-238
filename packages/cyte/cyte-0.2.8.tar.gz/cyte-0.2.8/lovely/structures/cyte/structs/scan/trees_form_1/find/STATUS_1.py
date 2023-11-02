




'''
	python3 status.py "structs/scan/trees_form_1/find/STATUS_1.py"
'''


import cyte.structs.scan.trees_form_1.find.region as find_region
import cyte.structs.DB.access as access
import cyte.structs.scan.trees_form_1 as trees_form_1


def check_1 ():
	struct_db = access.DB ()
	trees_form_1_grove = trees_form_1.start (struct_db)
	region = 1;

	struct = find_region.start (region, trees_form_1_grove)
	assert ('protein' in struct ['names']), struct

	struct = find_region.start (6, trees_form_1_grove)
	assert ('dietary fiber' in struct ['names']), struct


	return;
	
	
checks = {
	"trees form 1, find region": check_1
}