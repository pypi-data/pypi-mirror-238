

'''
	
'''

import cyte.hygiene._system.connect as connect
	
def start ():
	[ r, c ] = connect.start ()

	foods = r.db ('foods').table ('inventory')
	supps = r.db ('supplements').table ('inventory')

	foods_indexes = foods.index_list ().run (c)
	supps_indexes = foods.index_list ().run (c)
	
	
	
	return;