




'''
	python3 status.py "structs/scan/trees_form_1/for_each/STATUS_1.py"
'''


import cyte.structs.scan.trees_form_1.for_each as for_each
import cyte.structs.DB.access as access
import cyte.structs.scan.trees_form_1 as trees_form_1
	

import json

def structs_db_path ():
	import pathlib
	from os.path import dirname, join, normpath
	return normpath (join (pathlib.Path (__file__).parent.resolve (), "structs.json"))



def check_1 ():
	struct_db = access.DB (structs_db_path (), sort_keys = True)
	trees_form_1_grove = trees_form_1.start (struct_db)

	regions = []
	def for_each_fn (params):
		struct = params.struct;	
	
		regions.append (struct ["region"])

	for_each.start (
		trees_form_1_grove,
		for_each = for_each_fn
	)
	
	
	assert (
		[
			1, 2, 6, 7, 8, 3, 4, 5, 15, 51, 9, 12, 13, 14, 
			16, 17, 50, 52, 18, 19, 20, 21, 22, 23, 24, 25, 
			26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 
			38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 
			53, 54, 55, 56, 57, 58, 59, 60
		] == regions
	)
	
checks = {
	"structs trees_form_1 for each": check_1
}