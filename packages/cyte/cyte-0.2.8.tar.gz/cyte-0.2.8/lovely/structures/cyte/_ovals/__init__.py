

'''
	import cyte._ovals as ovals
	oval_ellipsis = ovals.find ()
'''

'''
	# USDA food
	import cyte._ovals as ovals
	API_USDA_ellipse = ovals.find () ['USDA'] ['food']
'''

'''
/online ellipsis/cyte/ellipsis.json 

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