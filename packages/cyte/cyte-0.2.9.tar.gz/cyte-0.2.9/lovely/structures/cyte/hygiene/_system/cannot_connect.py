
'''
import cyte.hygiene._system.cannot_connect as cannot_connect
cannot_connect.ensure (
	loops = 3
)
'''

import cyte.hygiene._system.connect as connect

def ensure (** keywords):
	loops = 5
	if ("loops" in keywords):
		loops = keywords ["loops"]

	could_not_connect = False
	try:
		[ r, c ] = connect.now (
			connect.parameters (
				loops = loops
			)
		)
		
		print ("Was able to connect, when should not have been able to connect")
		
	except Exception as E:	
		print (E)
		could_not_connect = True
		
	assert (could_not_connect == True)