

'''
python3 status_api.py "food/USDA/API/one/status/API_STATUS_foundational_1.py"
'''


import json

import cyte.food.USDA.API.one as USDA_food_API
import cyte._ovals as ovals


def CHECK_foundational_1 ():
	oval_ellipsis = ovals.find ()
	
	# 2346404
	food = USDA_food_API.find (
		2515381,
		API_ellipse = oval_ellipsis ["USDA"] ["food"],
		kind = "foundational"
	)
	
	#print (json.dumps (food ['data'], indent = 4))
	



	
checks = {
	"CHECK foundational 1": CHECK_foundational_1
}