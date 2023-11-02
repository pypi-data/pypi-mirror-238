
'''
	import cyte.food.USDA.examples as USDA_examples
	import cyte.food.USDA.struct_2 as USDA_struct_2
	walnuts_1882785 = USDA_struct_2.calc (
		USDA_examples.RETRIEVE ("branded/walnuts_1882785.json")
	)
'''

'''
	import cyte.food.USDA.examples as USDA_examples
	EXAMPLE = USDA_examples.RETRIEVE ("branded/BEET_JUICE_2642759.JSON")
'''


def RETRIEVE (PATH):
	import pathlib
	from os.path import dirname, join, normpath

	THIS_FOLDER = pathlib.Path (__file__).parent.resolve ()
	EXAMPLE = normpath (join (THIS_FOLDER, PATH))

	import json
	with open (EXAMPLE) as FP:
		data = json.load (FP)
	

	return data