

'''
	considerations:
		calories:
			-> e = m * (c ** 2) 
			-> m = e / (c **2)

		
		
'''



from fractions import Fraction

import cyte.mass.swap as mass_swap
import cyte.supplements.NIH.struct_2.ingredient.quantified.per.package as ingredient_quantified_per_package 
import cyte.supplements.NIH.struct_2.ingredient.quantified.per.form as ingredient_quantified_per_form

import json

def calc (
	ingredient, 
	NIH_supplement_data_struct_2
):
	print (NIH_supplement_data_struct_2 ['form'])

	quantity_of_form_per_package = NIH_supplement_data_struct_2 ["form"]["quantity"]
	form = NIH_supplement_data_struct_2 ["form"];
	ingredient_serving_size_quantity = ingredient ["quantity"][0]["servingSizeQuantity"]

	assert ("name" in ingredient)
	name = ingredient ["name"]


	[
		ingredient_unit,
		
		#
		#	quantity
		#
		ingredient_amount_per_form,
		ingredient_amount_per_form_float_string,
		
		#
		#	mass
		#
		fraction_per_form_in_grams,
		float_per_form_in_grams
	] = ingredient_quantified_per_form.calc (
		NIH_supplement_data_struct_2,
		ingredient
	) 
	
	'''
	print (ingredient["name"], [
		ingredient_unit,
		
		ingredient_amount_per_form,
		ingredient_amount_per_form_float_string,
		
		fraction_per_form_in_grams,
		float_per_form_in_grams,
		
		quantity_of_form_per_package
	])
	'''
		
	[ 
		fraction_per_package_in_grams,
		float_per_package_in_grams
	] = ingredient_quantified_per_package.calc (
		fraction_per_form_in_grams,
		quantity_of_form_per_package
	)
	
	#
	#	per serving calculations
	#	
	
	#
				# "fraction string grams": "97383/50000"
				#
	return {
		"name": name,
		
		"mass": {
			"per package": {
				"fraction string grams": str (fraction_per_package_in_grams),
				"float string grams": str (float_per_package_in_grams),
			},
			"per form": {
				"fraction string grams": str (fraction_per_form_in_grams),
				"float string grams": str (float_per_form_in_grams),
			},
			"per serving": {}
		},
		
		"quantity": {
			"per package": {
				"listed": {
					"unit": ingredient_unit
				}
			},
			"per form": {
				"listed": {
					"unit": ingredient_unit,
					"fraction string": str (ingredient_amount_per_form),
					"float string": ingredient_amount_per_form_float_string
				}
			}
		}
	}
	
	'''
	"quantity per form": {
			"form": form ["unit"],
			"amount": str (ingredient_amount_per_form),
			"unit": ingredient_unit
		},
		"quantity per form, in grams": {
			"form": form ["unit"],
			"amount": str (fraction_per_form_in_grams),
			"unit": "g"
		},
		"quantity per package, in grams": {
			"amount": str (fraction_per_package_in_grams),
			"unit": "g"
		},
	'''