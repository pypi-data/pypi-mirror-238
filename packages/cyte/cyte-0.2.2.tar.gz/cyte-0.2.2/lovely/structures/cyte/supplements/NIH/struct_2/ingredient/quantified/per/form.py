
from fractions import Fraction

import cyte.mass.swap as mass_swap

#
#	per form calculations
#
def calc (
	NIH_supplement_data_struct_2,
	ingredient
):
	defined = NIH_supplement_data_struct_2 ["defined"];
	form = NIH_supplement_data_struct_2 ["form"];
	ingredient_serving_size_quantity = ingredient ["quantity"][0]["servingSizeQuantity"]

	#
	#	make sure that the serving size quantity of the package
	#	is the same as the serving size quantity of the ingredient 
	#
	equal_serving_sizes = (
		ingredient_serving_size_quantity == 
		defined ["serving size"]["quantity"]
	)
	
	ingredient_unit = ingredient ["quantity"][0]["unit"]

	#
	#	ingredient amount per form = ingredient quantity / serving size quantity
	#
	ingredient_amount_per_form = ""
	if (
		len (ingredient ["quantity"]) == 1 and
		equal_serving_sizes
	):	
		ingredient_amount_per_form = Fraction (
			Fraction (ingredient ["quantity"][0]["quantity"]),
			Fraction (defined ["serving size"]["quantity"])
		)
		
	else:
		raise Exception ("Ingredient amount could not be calculated.")

	try:
		ingredient_amount_per_form_float_string = str (float (ingredient_amount_per_form))
	except Exception as E:
		ingredient_amount_per_form_float = "?"
	
	try:	
		fraction_per_form_in_grams = Fraction (mass_swap.START ([ 
			ingredient_amount_per_form, 
			ingredient_unit 
		], "grams"))
		
		#print ("fraction_per_form_in_grams:", name, fraction_per_form_in_grams)
		
	except Exception as E:
		print ("E:", E)
		fraction_per_form_in_grams = "?"
	
	try:
		float_per_form_in_grams = float (fraction_per_form_in_grams)
	except Exception as E:
		float_per_form_in_grams = "?"

	return [
		ingredient_unit,
		
		ingredient_amount_per_form,
		ingredient_amount_per_form_float_string,
		
		fraction_per_form_in_grams,
		float_per_form_in_grams
	]