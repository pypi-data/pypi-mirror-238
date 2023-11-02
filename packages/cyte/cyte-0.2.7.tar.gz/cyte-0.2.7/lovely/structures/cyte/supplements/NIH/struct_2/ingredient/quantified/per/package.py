

'''
	fraction_per_form_in_grams
	
	
	quantity_of_form_per_package
'''

from fractions import Fraction

#
#	per package calculations
#
def calc (
	fraction_per_form_in_grams,
	quantity_of_form_per_package
):
	try:
		fraction_per_package_in_grams = (
			Fraction (fraction_per_form_in_grams) * 
			Fraction (quantity_of_form_per_package)
		)
	except Exception as E:
		fraction_per_package_in_grams = "?"
		
	try:
		float_per_package_in_grams = float (fraction_per_package_in_grams)
	except Exception as E:
		float_per_package_in_grams = "?"

	return [
		fraction_per_package_in_grams,
		float_per_package_in_grams
	]