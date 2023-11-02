

'''
	checks:
		[  ] can connect
		[  ] has databases
		[  ] has tables 
		[  ] has secondary indexes
		
'''

import cyte.hygiene._system.connect as connect
	

def start ():
	[ r, c ] = connect.start ()

	db_list = r.db_list ().run (c)
	assert ("foods" in db_list)
	assert ("supplements" in db_list)
	assert ("recipes" in db_list)

	return;