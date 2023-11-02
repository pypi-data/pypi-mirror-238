

'''
	python3 status.py "recipes/struct_2/ingredients/quantified_grove/write/ingredients_in_grove_count/STATUS_1.py"
'''

import cyte.supplements.NIH.struct_2 as NIH_struct_2
import cyte.supplements.NIH.examples as NIH_examples

import cyte.recipes.struct_2.ingredients.quantified_grove.write.ingredients_in_grove_count as ingredients_in_grove_count

def check_1 ():
	chia_seeds_214893 = NIH_struct_2.calc (NIH_examples.RETRIEVE ("other/chia_seeds_214893.json"))

	count = ingredients_in_grove_count.start (
		quantified_grove = chia_seeds_214893 ["ingredients"]["quantified grove"]
	)

	assert (count == 21), count

	print ("count:", count)

	return;
	
	
checks = {
	"ingredients in grove count": check_1
}