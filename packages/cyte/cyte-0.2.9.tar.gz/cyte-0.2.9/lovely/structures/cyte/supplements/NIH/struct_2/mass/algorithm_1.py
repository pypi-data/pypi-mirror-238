
'''
	considerations:
		effectual
		calories - even with e = m * (c**2), these would be doubly added to the mass.
'''

'''
	"mass of quantified ingredients": {
		"caculated per package, ignoring IU": {
			
		}
	}
'''

from fractions import Fraction

def calc (NIH_SUPPLEMENT_data, RETURN):
	quantity_of_form = RETURN ["form"]["quantity"]
	quantified_ingredients = RETURN ["ingredients"]["quantified grove"]
	
	sum_mass_in_grams = 0
	
	skipped = []
	
	for ingredient in quantified_ingredients:
		try:
			mass_per_form_string = ingredient ["mass"] ["per form"] ["fraction string grams"]
			if (mass_per_form_string == ""):
				raise Exception ("")
			
			mass_per_form = Fraction (
				ingredient ["mass"] ["per form"] ["fraction string grams"]
			)
			
			sum_mass_in_grams += mass_per_form
			
		except Exception as E:
			skipped.append (ingredient ["name"])
						
			
	print ("skipped:", skipped)
	
	return {
		"sum of quantified ingredients, exluding effectual": {
			"skipped": skipped,
			"per package": {
				"fraction string grams": str (sum_mass_in_grams)
			},
			"per form": {
				"fraction string grams": str (
					Fraction (
						Fraction (sum_mass_in_grams), 
						Fraction (quantity_of_form)
					)
				),
			}
		}
	}
	
	"""	
		"caculated per package, ignoring IU, RAE, DFE, in grams": str (QUANTITY_IN_GRAMS),
		"caculated per form, ignoring IU, RAE, DFE in grams": str (Fraction (QUANTITY_IN_GRAMS, QUANTITY_OF_FORM)),
		"skipped": SKIPPED
	"""