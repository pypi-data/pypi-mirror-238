

'''
	python3 status.py "recipes/struct_2/ingredients/quantified_grove/aggregator/_status/STATUS_1.py"
'''



import cyte.supplements.NIH.struct_2 as NIH_struct_2
import cyte.supplements.NIH.examples as NIH_examples

import cyte.recipes.struct_2.ingredients.quantified_grove.aggregator as quantified_grove_aggregator

import cyte.structs.scan.trees_form_1 as trees_form_1
import cyte.structs.DB.access as access	
import cyte.structs.scan.trees_form_1.for_each as for_each

def check_1 ():
	chia_seeds_214893 = NIH_struct_2.calc (NIH_examples.RETRIEVE ("other/chia_seeds_214893.json"))



	chia_seeds_214893 ["product sequential"] = 1;

	def prepare_the_recipe_struct_grove ():
		recipe_struct_grove = trees_form_1.start (access.DB ())
	
		def for_each_fn (params):
			struct = params.struct;
			struct ["ingredients"] = []

		for_each.start (
			recipe_struct_grove,
			for_each = for_each_fn
		)	
		
		return recipe_struct_grove
		
		
	recipe_struct_grove = prepare_the_recipe_struct_grove ()
	
	returns = quantified_grove_aggregator.calc (
		recipe_struct_grove = recipe_struct_grove,
		product_quantified_grove = chia_seeds_214893 ["ingredients"] ["quantified grove"],
		product = chia_seeds_214893
	)
	
	product_structs_list = returns ["product structs list"]
	assert (len (product_structs_list) == 21)


	return;
	
	
checks = {
	"aggregator": check_1
}