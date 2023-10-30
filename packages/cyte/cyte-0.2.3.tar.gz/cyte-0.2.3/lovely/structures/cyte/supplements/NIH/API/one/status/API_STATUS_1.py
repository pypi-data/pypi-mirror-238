




'''
python3 status_api.py "supplements/NIH/API/one/status/STATUS_API_1.py"
'''

from BOTANY.IMPORT import IMPORT

import json

import cyte.supplements.NIH.API.one as NIH_API_one
	

def CHECK_branded_1 ():
	api_key = IMPORT ("/ONLINE_KEYS/NIH/__init__.py").keys () ["API"]
	supplement = NIH_API_one.find (220884, api_key)

	
checks = {
	"CHECK branded 1": CHECK_branded_1
}