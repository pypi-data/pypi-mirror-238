


'''
import cyte.recipes.struct_2.ingredients.quantified_grove.find.structs_list as structs_list
structs_list.start ()
'''

import cyte.structs.scan.names.has as struct_has_name
import json

def start (
	structs_db = None,
	product_quantified_grove = [], 
	level = 0,
	skipped = [],
	structs_list = [],
	product = {}
):
	indent = " " * (level * 4)
	product_quantified_grove.sort (
		key = lambda product_quantified_ingredient : product_quantified_ingredient ["name"][0]
	)

	for product_quantified_ingredient in product_quantified_grove:	
		try:
			struct = struct_has_name.search (
				structs_db,
				name = product_quantified_ingredient ['name']
			)
		except Exception as E:
			skipped.append (product_quantified_ingredient ['name'])
			return;
			
		mass_per_package_fraction_string_grams = "0"
		try:
			mass_per_package_fraction_string_grams = product_quantified_ingredient ["mass"] ["per package"] ["fraction string grams"]
		except Exception as E:
			print ("mass_per_package_fraction_string_grams Exception:", E)
		
			pass;	
		
		
		#print ("product name:", product ["product"]["name"])
		struct ["ingredient"] = {
			"sequential": product ["product sequential"],
			"product": product ["product"],
			"mass": {
				"per package": {
					"fraction string grams": mass_per_package_fraction_string_grams
				}
			}
		}
			
		structs_list.append (struct)

		#print (f"{ indent }{ product_quantified_ingredient ['name'] } : r{ struct ['region'] }")

		print (product_quantified_ingredient ['name'], len (product_quantified_ingredient ["quantified grove"]))

		if ("quantified grove" in product_quantified_ingredient):
			start (
				structs_db = structs_db,
				product_quantified_grove = product_quantified_ingredient ["quantified grove"], 
				level = (level + 1),
				skipped = skipped,
				structs_list = structs_list,
				product = product
			)