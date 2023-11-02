
'''
	priorities, plan:
		
		This should be for accessing the list of essential 
		nutrients, and the nutrients that they are comprised of.
		
		There could be another access point (like a rethinkdb weave
		access point) for accessing a network weave.
'''

'''
Accessing the core DB:

	import cyte.structs.DB.access as access
	structs_db = access.DB ()
'''

'''
Accessing another DB (replica, etc.):

	import cyte.structs.DB.access as access
	import cyte.structs.DB.PATH as structs_DB_PATH
	structs_DB = access.DB (
		PATH = structs_DB_PATH.find ()
	)
'''

from tinydb import TinyDB, Query
import cyte.structs.DB.PATH as structs_DB_PATH

def DB (
	PATH = structs_DB_PATH.find (),
	sort_keys = True
):
	DB = TinyDB (
		PATH, 
		sort_keys = sort_keys
	)
	
	return DB;