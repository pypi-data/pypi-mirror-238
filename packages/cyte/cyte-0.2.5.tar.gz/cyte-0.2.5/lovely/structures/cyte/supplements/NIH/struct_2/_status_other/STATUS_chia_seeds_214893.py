



'''
	python3 status.py "supplements/NIH/struct_2/_status_other/STATUS_chia_seeds_214893.py"
'''

'''
	https://www.amazon.com/PlantFusion-Supports-Mineralized-Supplement-90/dp/B07VP749CF
'''

import json
import cyte.supplements.NIH.examples as NIH_examples
import cyte.supplements.NIH.struct_2 as struct_2
import cyte._ensure.eq as equality
import cyte.supplements.NIH.struct_2.ingredient.quantified.find as find_quantified_ingredient

def CHECK_1 ():
	supplement_struct_2 = struct_2.calc (NIH_examples.RETRIEVE ("other/chia_seeds_214893.json"))
	
	from os.path import dirname, join, normpath
	import sys
	import pathlib
	import cyte._sculpt as sculpt
	sculpt.start (
		normpath (join (pathlib.Path (__file__).parent.resolve (), "struct_2_chia_seeds_214893.json")),
		json.dumps (supplement_struct_2, indent = 4)
	)
	
	
	quantified_ingredient = find_quantified_ingredient.start (
		quantified_grove = supplement_struct_2 ["ingredients"] ["quantified grove"],
		name = "potassium"
	)
		
	print ("quantified_ingredient:", json.dumps (quantified_ingredient, indent = 4))
	
checks = {
	"chia_seeds_214893": CHECK_1
}