

'''
import cyte.food.USDA.struct_2.ingredients.quantified_grove.printer as quantified_grove_printer
quantified_grove_printer.start ()
'''

def start (ingredients):
	return climb (ingredients)


def climb (ingredients, level = 0):
	spaces = " " * (level * 4)

	for ingredient in ingredients:
		print (f"{ spaces }{ ingredient ['name'] }")
		
		commodities = ingredient ['quantified grove']
		climb (commodities, level = (level + 1))
	
	
	return;


	
