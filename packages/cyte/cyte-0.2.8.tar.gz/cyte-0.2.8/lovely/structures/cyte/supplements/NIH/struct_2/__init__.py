


'''
import cyte.supplements.NIH.struct_2 as struct_2
supplement_struct_2 = struct_2.calc (nih_supplement_data)
'''

import cyte.supplements.NIH.struct_2.form as form 
import cyte.supplements.NIH.struct_2.form.unit as form_unit
import cyte.supplements.NIH.struct_2.defined.serving_size_quantity as defined_serving_size_quantity 
import cyte.supplements.NIH.struct_2.ingredients.quantified as INGREDIENTS_QUANTIFIED 
import cyte.supplements.NIH.struct_2.mass.algorithm_1 as mass_algorithm_1

import json

from fractions import Fraction

def calc (
	nih_supplement_data
):
	assert ("fullName" in nih_supplement_data)
	assert ("brandName" in nih_supplement_data)
	assert ("id" in nih_supplement_data)
	assert ("servingsPerContainer" in nih_supplement_data)

	nih_supplement_data_struct_2 = {
		"product": {
			"name":	nih_supplement_data ["fullName"],
			
			#
			#	Dietary Supplement Label Database
			#
			"DSLD ID": str (nih_supplement_data ["id"]),
			"UPC": nih_supplement_data ["upcSku"]			
		},
		
		"brand": {
			"name":	nih_supplement_data ["brandName"]
		},
		
		"statements": nih_supplement_data ["statements"],
		
		"form": {},
		
		#
		#	pertinent:
		#
		#		userGroups
		#
		#		servingSizes
		#
		"stated recommendations": {},
		
		"defined": {
			"servings per container": nih_supplement_data ["servingsPerContainer"],
			"serving size": {}
		},
		
		"ingredients": {
			"quantified grove": [],			
			"unquantified": []
		},
		
		"mass": {
			
		}
	}
	
	nih_supplement_data_struct_2 ["form"]["unit"] = form_unit.calc (nih_supplement_data)
	nih_supplement_data_struct_2 ["form"]["quantity"] = str (form.calc_QUANTITY (
		nih_supplement_data,
		nih_supplement_data_struct_2
	))
	
			
		
	

	nih_supplement_data_struct_2 [
		"defined"
	]["serving size"]["quantity"] = defined_serving_size_quantity.calc (
		nih_supplement_data,
		nih_supplement_data_struct_2
	)
	
	nih_supplement_data_struct_2 ["form"]["rounded"] = "?"
	if (
		nih_supplement_data_struct_2 ["form"]["unit"] == "gram"
	):
		is_rounded = nih_supplement_data_struct_2 ["form"]["quantity"] != (
			Fraction (nih_supplement_data_struct_2 ["defined"]["servings per container"]) *
			Fraction (nih_supplement_data_struct_2 ["defined"]["serving size"]["quantity"])
		)
	
		if (is_rounded):
			nih_supplement_data_struct_2 ["form"]["rounded"] = "yes"
	
	
	
	#print ("nih_supplement_data_struct_2:", json.dumps (nih_supplement_data_struct_2, indent = 4))
	
	nih_supplement_data_struct_2 ["ingredients"]["quantified grove"] = INGREDIENTS_QUANTIFIED.calc (
		nih_supplement_data,
		nih_supplement_data_struct_2
	)
	
	nih_supplement_data_struct_2 ["ingredients"]["unquantified"] = nih_supplement_data [
		"otheringredients"
	] [ "ingredients" ]
	
	
	calculated_masses = mass_algorithm_1.calc (
		nih_supplement_data, 
		nih_supplement_data_struct_2
	)
	print ("calculated_masses masses", calculated_masses)
	
	for calculated in calculated_masses:
		nih_supplement_data_struct_2 ["mass"][ calculated ] = calculated_masses [ calculated ]

	return nih_supplement_data_struct_2