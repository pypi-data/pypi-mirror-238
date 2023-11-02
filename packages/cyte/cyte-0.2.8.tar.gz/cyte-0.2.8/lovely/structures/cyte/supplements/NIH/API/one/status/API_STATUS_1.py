




'''
python3 status_api.py "supplements/NIH/API/one/status/STATUS_API_1.py"
'''


import json

import cyte.supplements.NIH.API.one as NIH_API_one
import cyte._ovals as ovals	

def CHECK_branded_1 ():
	oval_ellipsis = ovals.find ()
	supplement = NIH_API_one.find (220884, oval_ellipsis ["NIH"] ["supplements"])

	
checks = {
	"NIH branded 1": CHECK_branded_1
}