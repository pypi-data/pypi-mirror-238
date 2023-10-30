

'''
import cyte.supplements.NIH.struct_2.ingredient.quantified.find as find_quantified_ingredient
find_quantified_ingredient.start (
	quantified_grove = product ["ingredients"] ["quantified grove"],
	name = ""
)
'''


def traverse (name, grove):
	for ingredient in grove:	
		#print ("name:", ingredient ['name'])
	
		if (ingredient ['name'].lower () == name.lower ()):
			return ingredient;

		if (len (ingredient ["quantified grove"]) >= 1):
			returns = traverse (name, ingredient ["quantified grove"])			
			if (type (returns) == dict):
				return returns;
				
	return False


def start (name, quantified_grove):
	returns = traverse (name, quantified_grove)
	if (returns == False):
		raise Exception (f"Name '{ name }' was not found.")
	
	return returns

