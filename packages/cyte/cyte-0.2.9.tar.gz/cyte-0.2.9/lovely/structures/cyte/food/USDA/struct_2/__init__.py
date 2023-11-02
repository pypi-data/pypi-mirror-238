

import cyte._interpret.unit_kind as UNIT_kind

import cyte.food.USDA.struct_2.energy as ENERGY
import cyte.food.USDA.struct_2.ingredients.quantified_list as quantified_list
import cyte.food.USDA.struct_2.ingredients.quantified_grove as quantified_grove
import cyte.food.USDA.struct_2.mass as mass
import cyte.food.USDA.struct_2.packageWeight as package_weight
import cyte.food.USDA.struct_2.servings as SERVINGS

from fractions import Fraction

def calc (usda_food_data):
	returns = {
		"product": {
			"name":	usda_food_data ["description"],
			"FDC ID": str (usda_food_data ["fdcId"]),
			"UPC": usda_food_data ["gtinUpc"]			
		},
		
		"brand": {
			"name":	usda_food_data ["brandName"],
			"owner": usda_food_data ["brandOwner"]
		},
		
		"defined": {
			"servings per package": {},
			"serving size": {
				"unit": usda_food_data ["servingSizeUnit"],
				"amount": str (usda_food_data ["servingSize"]),
				"kind": UNIT_kind.calc (usda_food_data ["servingSizeUnit"])
			},
			"quantity": {
				"reported": usda_food_data ["packageWeight"],
				"notes": "This could be the 'mass' and or 'volume', etc."
			}			
		},
		
		"mass": {},
		"volume": {},
	
		"ingredients": {
			"quantified list": [],
			"quantified grove": [],
			
			"unquantified": [],
			"unquantified string": usda_food_data ["ingredients"]
		}
		
	}
	
	interpretted_package_weight = package_weight.INTERPRET (usda_food_data)
	if ("mass" in interpretted_package_weight):
		returns ["mass"] = interpretted_package_weight ["mass"]

	if ("volume" in interpretted_package_weight):
		returns ["volume"] = interpretted_package_weight ["volume"]

	returns ["defined"] ["servings per package, fraction string"] = SERVINGS.calc (usda_food_data, returns)
	returns ["defined"] [
		"servings per package, float string"
	] = str (float (Fraction (returns ["defined"] ["servings per package, fraction string"])))


	returns ["ingredients"]["quantified list"] = quantified_list.calc (
		usda_food_data,
		returns
	)
	returns ["ingredients"]["quantified grove"] = quantified_grove.calc (
		usda_food_data,
		returns
	)

	#
	#	todo: sum the masses of the grove
	#
	'''
		mass: {
			"of quantified ingredients, excluding effectual":
			"of quantified ingredients, including effectual":
		}
	'''
	
	
	'''
		todo:
			[ ] 
			ingredient {
				"mass": {
					
					#
					#	if (
					#		package mass is known,
					#		ingredient mass is known
					#	):
					#
					"'ingredient mass' / 'package mass'": "?",
					
					
					#
					#
					#
					"'ingredient mass' / 'summation (quantified ingredient mass, excluding effectual masses)'": 
					
					
					#
					#
					#
					"'ingredient mass' / 'summation (quantified ingredient effectual mass)'": 					
				}
			}
	'''


	return returns