

'''
import hygiene.foods.inventory.doc_examples.add as add_food
add_food.hastily (
	name = ".json",
	document = document
)
'''

import pathlib
from os.path import dirname, join, normpath

def hastily (
	name,
	document
):
	this_directory = pathlib.Path (__file__).parent.resolve ()
	this_path = normpath (join (this_directory, name))

	import json

	fp = open (this_path, "w")
	fp.write (json.dumps (document, indent = 4))
	fp.close ()
	