
'''
	import cyte.food.NIH.examples as NIH_examples
	EXAMPLE = NIH_examples.RETRIEVE ("tablets/multivitamin_249664.JSON")
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