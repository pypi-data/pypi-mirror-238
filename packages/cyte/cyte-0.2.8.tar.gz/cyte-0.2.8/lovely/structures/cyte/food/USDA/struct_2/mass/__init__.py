

'''
from cyte.USDA.struct_2.quantity 
'''

'''
	"12 fl oz/355 mL"
'''

'''
	1 mL == 
'''

import cyte.food.USDA.struct_2.packageWeight.interpret as PACKAGE_WEIGHT

def calc (usda_food_data):
	assert ("packageWeight" in usda_food_data)

	RETURN = {
		"per package": {
			"grams": ""
		}
	}

	PARSED_WEIGHT = PACKAGE_WEIGHT.INTERPRET (usda_food_data ["packageWeight"])
	print (PARSED_WEIGHT)

	return;