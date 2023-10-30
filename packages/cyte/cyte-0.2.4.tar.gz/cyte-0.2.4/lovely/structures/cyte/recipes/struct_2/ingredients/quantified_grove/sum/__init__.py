

'''
{
    "includes": [],
    "names": [
        "vitamin d"
    ],
    "region": 60,
    "includes structs": [],
    "ingredients": [
        {
            "sequential": 1,
            "product": {
                "name": "Chia Seeds",
                "DSLD": "214893",
                "UPC": "8 18423 02863 7"
            },
            "mass": {
                "per package": {
                    "fraction string grams": "0"
                }
            }
        }
    ]
}
'''

import cyte.structs.scan.trees_form_1.for_each as for_each

from fractions import Fraction

def calc (
	recipe_struct_grove
):
	def for_each_fn (params):
		struct = params.struct;
	
		import json
		#print ("recipe struct:", json.dumps (struct, indent = 4))

		mass_grams_sum = 0
		ingredients = struct ["ingredients"]
		for ingredient in ingredients:
			try:
				mass_per_package_fraction_grams = Fraction (
					ingredient ["mass"] ["per package"] ["fraction string grams"]
				)
			
			except Exception as E:
				mass_per_package_fraction_grams = 0
			
			mass_grams_sum += mass_per_package_fraction_grams
		
		if ("mass" not in struct):
			struct ["mass"] = {}
			
		if ("per package" not in struct ["mass"]):
			struct ["mass"] ["per package"] = {}
			
		struct ["mass"] ["per package"] ["fraction string grams"] = str (mass_grams_sum)
		struct ["mass"] ["per package"] ["float string grams"] = str (float (mass_grams_sum))
		
			

	for_each.start (
		recipe_struct_grove,
		for_each = for_each_fn
	)

	return;