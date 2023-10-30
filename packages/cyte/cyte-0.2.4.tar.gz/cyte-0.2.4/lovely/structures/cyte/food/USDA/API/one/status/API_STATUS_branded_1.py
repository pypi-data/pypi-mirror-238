

'''
python3 status_api.py "food/USDA/API/one/status/API_STATUS_branded_1.py"
'''

from BOTANY.IMPORT import IMPORT

import json

import cyte.food.USDA.API.one as USDA_food_API
import cyte._ovals as ovals


def CHECK_branded_1 ():
	#KEYS = IMPORT ("/online ellipsis/USDA/__init__.py").KEYS ()
	
	oval_ellipsis = ovals.find ()
	
	food = USDA_food_API.find (
		2642759,
		API_ellipse = oval_ellipsis ["USDA"] ["food"]
	)

	
checks = {
	"CHECK branded 1": CHECK_branded_1
}