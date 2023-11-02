

'''
import cyte.recipes.struct_2 as struct_2_recipes
import cyte.structs.DB.access as access
import cyte.structs.scan.trees_form_1 as trees_form_1

struct_2_recipes.calc ({
	#
	#	struct 2 products
	#
	"products": [
		{
			"product": { "FDC ID": "" }
		},
		{
			"product": { "DSLD": "" }
		}
	],
	"structs grove": trees_form_1.start (access.DB ())
})
'''


import cyte.recipes.struct_2.ingredients.quantified_grove.aggregator as quantified_grove_aggregator
import cyte.recipes.struct_2.ingredients.quantified_grove.sum as quantified_grove_sum


import cyte.structs.scan.trees_form_1.for_each as for_each
import cyte.structs.scan.trees_form_1 as trees_form_1
import cyte.structs.DB.access as access

def calc (delivery):
	products = delivery ["products"]
	#structs_grove = delivery ["structs grove"]
	
	product_count = 1
	for product in products:
		product ["product sequential"] = product_count;
		product_count += 1
	
	'''
		attach [nih,usda] ingredient groves to struct trees_form_1
		
			example:
				data:
					walnuts, 20g
						dietary fiber, 7g
					
					lentils, 28g
						carbs 12g
							dietary fiber, 6g
							
				trees_form_1
					carbohydrates [not found]
						dietary fiber, 7g
						
					carbohydrates 12g
						dietary fiber, 6g
						
				add summation of descend struct masses to ascendent structs if not found.
					carbohydrates 7g
						dietary fiber, 7g
						
					carbohydrates 12g
						dietary fiber, 6g
	'''
	
	
	'''
		{
			"ingredients": {
				"quantified grove": [{
					"mass": {
						"per package": {
							"fraction string grams": "80613964204970697/28147497671065600",
							"float string grams": "2.8639833333333335"
						}
					}
				}]
			}
		}
	
		[{
			"names": ["protein"], 
			"region": 1,
			"includes": [], 
			"products": [{
				"sequential": 1,
				"product": {
					"name": "WALNUTS HALVES & PIECES, WALNUTS",
					"FDC ID": "1882785",
					"UPC": "099482434618"
				},
				"mass": {
					"per package": {
						"fraction string grams": "80613964204970697/28147497671065600",
					}
				}
			}]
		}]
	'''
	
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
	
	counter_1 = 0
	for product in products:
		counter_1 += 1
	
		#print ()
		#print ()
		#print ("combining:", counter_1)
		#print ()
		#print ()
	
		quantified_grove_aggregator.calc (
			recipe_struct_grove,
			product ["ingredients"]["quantified grove"],
			product
		)

	quantified_grove_sum.calc (recipe_struct_grove)

	def for_each_fn (params):
		struct = params.struct;
		import json
		#print ("recipe struct:", json.dumps (struct, indent = 4))

	for_each.start (
		recipe_struct_grove,
		for_each = for_each_fn
	)	

	class recipe:
		def __init__ (this, recipe_struct_grove):
			this.recipe_struct_grove = recipe_struct_grove

	return recipe (
		recipe_struct_grove
	)