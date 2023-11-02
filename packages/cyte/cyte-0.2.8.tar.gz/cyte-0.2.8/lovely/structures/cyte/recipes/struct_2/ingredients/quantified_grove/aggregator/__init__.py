
'''
This adds products to the recipe.

Currently it also adds products to a skipped list.


'''



'''
import cyte.recipes.struct_2.ingredients.quantified_grove.aggregator as quantified_grove_aggregator
quantified_grove_aggregator.calc (
	recipe_quantified_grove = [],
	product_quantified_grove = []
)
'''

'''
	steps:
		1. create a flat list of structs from the product "quantified grove"
		
		2. attach (merge) the product structs to the "product struct grove"
			* if not in "product struct grove", then skip.
		
			1. make sure that there aren't any missing intermediaries
		
		3. merge the product struct grove into the recipe struct grove
'''


import json
	
import cyte.recipes.struct_2.ingredients.quantified_grove.find.structs_list as find_structs_list

import cyte.structs.DB.access as access
import cyte.structs.scan.names.has as struct_has_name
import cyte.structs.scan.trees_form_1 as trees_form_1
import cyte.structs.scan.trees_form_1.attach as attach_product_struct
import cyte.structs.scan.trees_form_1.for_each as for_each
import cyte.structs.scan.trees_form_1.find.region as find_region
import cyte.structs.scan.trees_form_1.printer as trees_form_1_printer

def calc (
	recipe_struct_grove,
	product_quantified_grove,
	product
):
	skipped = []
	product_ingredients_structs_list = []
	structs_db_1 = access.DB ()

	#print ("product_quantified_grove:", json.dumps (product_quantified_grove, indent = 4))
	#return;

	find_structs_list.start (
		structs_db = structs_db_1,
		product_quantified_grove = product_quantified_grove,
		structs_list = product_ingredients_structs_list,
		skipped = skipped,
		product = product
	)

	print ("structs found:");
	for product_ingredient_struct in product_ingredients_structs_list:
		print (" ", product_ingredient_struct ["names"])

	
	#
	#	todo:
	#
	print ("skipped:", json.dumps (skipped, indent = 4))

	#
	#	structs_db_1 dict shouldn't be modified, but in case it is,
	#	utilize a difference one.
	#
	structs_db_2 = access.DB ()
	product_struct_grove = trees_form_1.start (structs_db_2)
	trees_form_1_printer.write (product_struct_grove)

	#
	#	attach (merge) the "product structs" to the "structs tree form 1"
	#
	for product_struct in product_ingredients_structs_list:
		print ("product_struct ::", product_struct)
		
		attach_product_struct.start (
			product_struct, 
			product_struct_grove
		)

	#
	#	make sure all ascendants were found, if there's a product
	#	attached to the grove struct.
	#
	#	An exception would imply that something like:
	#		Carbs - found
	#			Sugars - not found
	#				Added Sugars - found
	#
	#		where "Sugars" is not in the quantified ingredients
	#		of the product, but it is in the structs tree.
	#
	def is_missing_intermediaries (
		structs, 
		level = 0, 
		ascendents_line = []
	):
		indent = " " * (level * 4)
		structs.sort (key = lambda struct : struct ["names"][0])

		for struct in structs:
			if ("found" in struct):
				found = struct ['found']
				ascendents_line.append ({
					"struct": struct,
					"found": True
				})
			else:
				found = "no "
				ascendents_line.append ({
					"struct": struct,
					"found": False
				})
			
			#
			#	make sure all ascendants were found, if there's a product
			#	attached to the grove
			#
			#	An exception would imply that something like:
			#		Carbs - found
			#			Sugars - not found
			#				Added Sugars - found
			#
			#		where "Sugars" is not in the quantified ingredients
			#		of the product, but it is in the structs tree.
			#
			if (found == True):
				for ascendent in ascendents_line:
					assert (ascendent ["found"] == True), ascendents_line
				
			print (f"{ indent }[{ found }] { struct['names'] } { struct['region'] }")

			if ("includes structs" in struct):
				is_missing_intermediaries (
					struct ["includes structs"], 
					level = (level + 1),
					ascendents_line = ascendents_line
				)

	is_missing_intermediaries (product_struct_grove)
	
	#
	'''
		Loop through the product_struct_grove
		and aggregate each product into the
		recipe_struct_grove.
	'''
	def for_each_fn (params):
		product_struct = params.struct;
			
		if ("found" in product_struct and product_struct ["found"] == "yes"):
			product_struct_region = product_struct ["region"]
		
			recipe_struct = find_region.start (
				product_struct_region, 
				recipe_struct_grove
			)
			
			#print ("product struct:", json.dumps (product_struct, indent = 4))
			
			
			recipe_struct ["ingredients"].append (product_struct ["ingredient"])
			
			'''
			mass_per_package_fraction_string_grams = "0"
			try:
				mass_per_package_fraction_string_grams = product_struct [""]
			except Exception as E:
				pass;
			
			recipe_struct.append ({
				"ellipse": 1,
				"mass": {
					"per package": {
						"fraction string grams": mass_per_package_fraction_string_grams
					}
				}
			})
			'''

	for_each.start (
		product_struct_grove,
		for_each = for_each_fn
	)	
	
	
	return {
		"product structs list": product_ingredients_structs_list
	}