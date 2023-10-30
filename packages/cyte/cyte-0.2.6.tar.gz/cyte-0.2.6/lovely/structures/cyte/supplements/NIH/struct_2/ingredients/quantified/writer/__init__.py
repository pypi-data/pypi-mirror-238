

'''
import cyte.supplements.NIH.API.one as NIH_API_one
NIH_supplement = NIH_API_one.find (dsld_id)

import cyte.supplements.NIH.struct_2.ingredients.quantified.writer as quantified_ingredient_writer
quantified_ingredient_writer.write (NIH_supplement ["data"])
'''

import cyte.structs.scan.names.has as struct_has_name

import json

def print_grove (
	nih_structs, 
	structs_db = None,
	level = 0
):
	indent = " " * (level * 4)
	nih_structs.sort (key = lambda nih_struct : nih_struct ["name"][0])

	for nih_struct in nih_structs:	
		struct = struct_has_name.search (
			structs_db,
			name = nih_struct ['name']
		)

		print (f"{ indent }{ nih_struct ['name'] } : r{ struct ['region'] }")

		if ("nestedRows" in nih_struct):
			print_grove (
				nih_struct ["nestedRows"], 
				level = (level + 1),
				
				structs_db = structs_db
			)

def write (
	NIH_supplement_data,
	structs_db
):
	assert ("ingredientRows" in NIH_supplement_data)

	ingrdient_rows = NIH_supplement_data ["ingredientRows"]
	ingrdient_rows.sort (key = lambda ingredient : ingredient ["name"])
	
	print_grove (ingrdient_rows, structs_db = structs_db)
	


