



'''
	python3 status.py "food/USDA/struct_2/_status_liquids/STATUS_beet_juice_2412474.py"
'''

import json

import cyte.food.USDA.examples as USDA_examples
import cyte.food.USDA.struct_2 as USDA_struct_2

import cyte._ensure.eq as equality

def CHECK_1 ():
	food_struct_2 = USDA_struct_2.calc (
		USDA_examples.RETRIEVE ("branded/BEET_JUICE_2412474.JSON")
	)
	
	#import pyjsonviewer
	#pyjsonviewer.view_data (json_data = food_struct_2)

	assert (food_struct_2 ["volume"]["per package, in liters"] == "0.473176")
	assert (
		food_struct_2 ["ingredients"]["unquantified string"] == 
		"BEET, CITRIC ACID"
	)
	
	
	equality.check (1, 1)
	
	from os.path import dirname, join, normpath
	import sys
	import pathlib
	import cyte._sculpt as sculpt
	sculpt.start (
		normpath (join (pathlib.Path (__file__).parent.resolve (), "struct_2_beet_juice_2412474.json")),
		json.dumps (food_struct_2, indent = 4)
	)
	
checks = {
	"BEET JUICE 2642759": CHECK_1
}


