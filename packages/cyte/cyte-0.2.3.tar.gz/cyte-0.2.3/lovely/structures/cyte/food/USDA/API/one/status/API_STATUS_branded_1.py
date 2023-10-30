

'''
python3 status_api.py "food/USDA/API/one/status/API_STATUS_branded_1.py"
'''

from BOTANY.IMPORT import IMPORT

import json

import cyte.food.USDA.API.one as USDA_food_API

def CHECK_branded_1 ():
	KEYS = IMPORT ("/ONLINE_KEYS/USDA/__init__.py").KEYS ()
	food = USDA_food_API.find (
		2642759,
		API_ellipse = KEYS ["API"]
	)

	
checks = {
	"CHECK branded 1": CHECK_branded_1
}