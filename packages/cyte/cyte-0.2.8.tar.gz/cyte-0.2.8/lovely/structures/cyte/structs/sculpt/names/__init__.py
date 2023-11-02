


'''
import cyte.structs.DB.access as access
import cyte.structs.sculpt.names as sculpt_names

struct_DB = access.DB ()
sculpt_names.START (
	struct_DB,
	REGION = 10000,
	names = []
)
'''


from tinydb import TinyDB, Query

def START (
	sculpt_DB,
	REGION,
	names
):
	Q = Query ()
	sculpt_DB.update (
		{ 
			'names': names
		}, 
		Q.region == REGION
	)

	return;