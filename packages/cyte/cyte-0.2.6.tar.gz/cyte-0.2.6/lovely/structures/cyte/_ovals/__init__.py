

'''
import cyte._ovals as ovals
oval_ellipsis = ovals.find ()
'''

'''
import cyte._ovals as ovals
API_USDA_ellipse = ovals.find () ['USDA'] ['food']
'''

'''
{
	"USDA": {
		"food": ""
	},
	"NIH": {
		"supplements": ""
	}
}
'''

import json
fp = open ("/online ellipsis/cyte/ellipsis.json", "r")
ellipsis = json.loads (fp.read ())
fp.close ()


def find ():
	return ellipsis