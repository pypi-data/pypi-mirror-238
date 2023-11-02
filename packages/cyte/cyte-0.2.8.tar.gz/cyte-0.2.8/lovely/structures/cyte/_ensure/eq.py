

'''
import cyte._ensure.eq as equality
equality.check (1, 1)
'''

import json
def check (ONE, TWO):
	if (ONE != TWO):
		ONE_STRING = ONE
		if (type (ONE) == dict):
			ONE_STRING = json.dumps (ONE, indent = 4)
		
		TWO_STRING = TWO
		if (type (TWO) == dict):
			TWO_STRING = json.dumps (TWO, indent = 4)
	
		raise Exception (f'"{ ONE_STRING }" != "{ TWO_STRING }"')

	return