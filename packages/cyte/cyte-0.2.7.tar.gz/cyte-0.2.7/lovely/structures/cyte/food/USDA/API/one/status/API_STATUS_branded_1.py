

'''
python3 status_api.py "food/USDA/API/one/status/API_STATUS_branded_1.py"
'''

import json

import cyte.food.USDA.API.one as USDA_food_API



def CHECK_branded_1 ():	
	import cyte._ovals as ovals
	oval_ellipsis = ovals.find ()
	food_ellipse = oval_ellipsis ["USDA"] ["food"]
	
	food = USDA_food_API.find (
		2642759,
		API_ellipse = food_ellipse
	)

	
checks = {
	"CHECK branded 1": CHECK_branded_1
}