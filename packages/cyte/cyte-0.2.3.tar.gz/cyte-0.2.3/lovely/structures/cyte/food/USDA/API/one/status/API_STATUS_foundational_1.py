

'''
python3 status_api.py "food/USDA/API/one/status/API_STATUS_foundational_1.py"
'''

from BOTANY.IMPORT import IMPORT

import json

import cyte.food.USDA.API.one as USDA_food_API


def CHECK_foundational_1 ():
	KEYS = IMPORT ("/ONLINE_KEYS/USDA/__init__.py").KEYS ()
	
	# 2346404
	food = USDA_food_API.find (
		2515381,
		API_ellipse = KEYS ["API"],
		kind = "foundational"
	)
	
	#print (json.dumps (food ['data'], indent = 4))
	



	
checks = {
	"CHECK foundational 1": CHECK_foundational_1
}