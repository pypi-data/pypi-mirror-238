

'''
	python3 status.py "recipes/struct_2/_status/2_2_ingredients/STATUS_recipe.py"
'''

'''
	零: 0
	一: 1
	二: 2
	三: 3
	四: 4
	五: 5
	六: 6
	七: 7
	八: 8
	九: 9
	十: 10
	
	朋友: friend
	梦: dreams
	梦想: dream
	钱: money
'''

import cyte.food.USDA.examples as USDA_examples
import cyte.food.USDA.struct_2 as USDA_struct_2

import cyte.supplements.NIH.examples as NIH_examples
import cyte.supplements.NIH.struct_2 as struct_2

import cyte.recipes.struct_2 as struct_2_recipes

import cyte.structs.scan.trees_form_1.find.region as find_region

import json

def check_1 ():	
	walnuts_1882785 = USDA_struct_2.calc (
		USDA_examples.RETRIEVE ("branded/walnuts_1882785.json")
	)	
	calcium_261967 = struct_2.calc (
		NIH_examples.RETRIEVE ("tablets/calcium_261967.JSON")
	)
	chia_seeds_214893 = struct_2.calc (NIH_examples.RETRIEVE ("other/chia_seeds_214893.json"))
	
	recipe = struct_2_recipes.calc ({
		"products": [
			chia_seeds_214893,
			chia_seeds_214893
		]
	})
	
	recipe_struct_grove = recipe.recipe_struct_grove;
	
	from os.path import dirname, join, normpath
	import sys
	import pathlib
	import cyte._sculpt as sculpt
	sculpt.start (
		normpath (join (pathlib.Path (__file__).parent.resolve (), "recipe_struct_grove.json")),
		json.dumps (recipe_struct_grove, indent = 4)
	)
	
	vitamin_d = find_region.start (60, recipe_struct_grove)
	#print ("vitamin d:", json.dumps (struct, indent = 4))
	assert (
		vitamin_d ["ingredients"][0]["mass"]["per package"]["fraction string grams"] ==
		"0"	
	), vitamin_d
	assert (
		vitamin_d ["mass"]["per package"]["fraction string grams"] ==
		"0"	
	), vitamin_d
	
	
	def protein ():
		ingredient = find_region.start (1, recipe_struct_grove)
		assert (
			ingredient ["ingredients"][0]["mass"]["per package"]["fraction string grams"] ==
			"227/3"
		)
		assert (
			ingredient ["ingredients"][0]["mass"]["per package"]["fraction string grams"] ==
			"227/3"
		)
		assert (
			ingredient ["mass"]["per package"]["fraction string grams"] ==
			"454/3"
		)
	protein ()

	return;
	
	
	
checks = {
	"recipe with 1 product": check_1
}