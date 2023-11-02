

'''
	python3 status.py "recipes/struct_2/ingredients/quantified_grove/write/ingredients_in_grove_count/STATUS_1.py"
'''

import cyte.supplements.NIH.struct_2 as NIH_struct_2
import cyte.supplements.NIH.examples as NIH_examples

import cyte.food.USDA.examples as USDA_examples
import cyte.food.USDA.struct_2 as USDA_struct_2

import cyte.recipes.struct_2.ingredients.quantified_grove.write.ingredients_in_grove_count as ingredients_in_grove_count

def check_1 ():
	walnuts_1882785 = USDA_struct_2.calc (
		USDA_examples.RETRIEVE ("branded/walnuts_1882785.json")
	)

	count = ingredients_in_grove_count.start (
		quantified_grove = walnuts_1882785 ["ingredients"]["quantified grove"]
	)

	assert (count == 16), count

	print ("count:", count)

	return;
	
	
checks = {
	"ingredients in grove count for food": check_1
}