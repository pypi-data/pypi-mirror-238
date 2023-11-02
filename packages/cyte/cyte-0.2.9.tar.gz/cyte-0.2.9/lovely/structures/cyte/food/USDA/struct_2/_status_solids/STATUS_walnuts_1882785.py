


'''
https://fdc.nal.usda.gov/fdc-app.html#/food-details/1882785/nutrients
'''



'''
	python3 status.py "food/USDA/struct_2/_status/STATUS_walnuts_1882785.py"
'''

import json

import cyte.food.USDA.examples as USDA_examples

import cyte.food.USDA.struct_2 as USDA_struct_2
import cyte.food.USDA.struct_2.ingredients.quantified_grove.printer as quantified_grove_printer

import cyte._ensure.eq as equality

def CHECK_1 ():
	food_struct_2 = USDA_struct_2.calc (
		USDA_examples.RETRIEVE ("branded/walnuts_1882785.json")
	)
	
	print (json.dumps (food_struct_2, indent = 4))

	#import pyjsonviewer
	#pyjsonviewer.view_data (json_data = food_struct_2)
	
	ingredients_quantified_grove = food_struct_2 ["ingredients"]["quantified grove"]
	quantified_grove_printer.start (ingredients_quantified_grove)
	
	#
	#	equality checks
	#
	
	equality.check (food_struct_2 ["defined"]["serving size"]["kind"], "mass")
	equality.check (food_struct_2 ["defined"]["serving size"]["amount"], "28")
	equality.check (food_struct_2 ["defined"]["serving size"]["unit"], "g")
	equality.check (food_struct_2 ["defined"]["servings per package, fraction string"], "227/14")
	
	
	equality.check (food_struct_2 ["mass"]["per package, in grams"], "454")
	
	equality.check (
		len (food_struct_2 ["ingredients"]["quantified list"]),
		16
	)
	equality.check (
		len (food_struct_2 ["ingredients"]["quantified grove"]),
		10
	)
	
	from os.path import dirname, join, normpath
	import sys
	import pathlib
	import cyte._sculpt as sculpt
	sculpt.start (
		normpath (join (pathlib.Path (__file__).parent.resolve (), "struct_2_walnuts_1882785.json")),
		json.dumps (food_struct_2, indent = 4)
	)
	
	
checks = {
	"walnuts 1882785": CHECK_1
}


