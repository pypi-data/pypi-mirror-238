

'''
import cyte.food.USDA.struct_2.ingredients.quantified_grove as quantified_grove

'''

import copy

def is_included (region, list):
	for commodity in list:
		includes = commodity ["struct"] ["includes"]
	
		for included in includes:
			if (included == region):
				return [ True, commodity ]

	return [ False, "" ]

def calc (
	usda_food_data,
	RETURN
):
	list = copy.deepcopy (
		RETURN ["ingredients"]["quantified list"]
	)
	
	#directional_links = 
	
	#import cyte.structs.scan.trees_form_1 as trees_form_1
	#trees = trees_form_1.start (struct_DB)
	
	for ingredient in list:
		ingredient ["quantified grove"] = []
	
	grove = []
	
	selector = 0
	while (selector <= len (list) - 1):
		ingredient = list [selector]
	
		region = ingredient ["struct"]["region"]
	
		#print (
		#	ingredient ["struct"] ["names"], 
		#	ingredient ["struct"] ["includes"]
		#)
	
		[ included, commodity ] = is_included (
			ingredient ["struct"]["region"],
			list
		)
		if (included == True):
			commodity ["quantified grove"].append (
				copy.deepcopy (ingredient)
			)
			list.remove (ingredient)
		
		selector += 1
			
		
		print (region, "included:", included)
	
	return list