
'''
	"packageWeight": "12 oz/340 g",
		
		"mass": {
			"per package, in grams": ,
			
			"per package": [{
				"unit": [ "gram" ],
				"amount": 
			}]
		}
		
	
	"packageWeight": "12 fl oz/355 mL",
	
		"volume": {
			"per package": [{
				"unit": [ "liter" ],
				"amount": 
			}]
		}
'''

'''
possibilities:
	"quantity per package": {
		"system international": {
			"grams float": "113.0",
			"grams fraction": "113/1",
			"grams e note": "113.00e0",
			"grams base 10": "113.00 * (10^0)"
		},
		"us customary": {
			"pounds float": "0.25"
		}
	}
'''

import cyte.food.USDA.struct_2.packageWeight.interpret as interpreter

def INTERPRET (usda_food_data):
	assert ("packageWeight" in usda_food_data)
	
	RETURN = {}
	PARSED = interpreter.INTERPRET (usda_food_data ["packageWeight"])
	print ("PARSED:", PARSED)

	if ("LITERS" in PARSED):
		RETURN ["volume"] = {
			"per package calculated": "yes",
			"per package, in liters": PARSED ["LITERS"]
		}
	else:
		RETURN ["volume"] = {
			"per package calculated": "no"
		}
		
	if ("GRAMS" in PARSED):
		RETURN ["mass"] = {
			"per package calculated": "yes",
			"per package, in grams": PARSED ["GRAMS"]
		}
	else:
		RETURN ["mass"] = {
			"per package calculated": "no"
		}

	return RETURN