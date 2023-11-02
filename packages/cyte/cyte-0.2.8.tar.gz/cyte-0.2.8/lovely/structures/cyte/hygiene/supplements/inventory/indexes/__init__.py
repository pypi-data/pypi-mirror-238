
'''
import cyte.hygiene.supplements.inventory.indexes as foods_indexes

'''
import cyte.hygiene._system.connect as connect

def create ():
	[ r, c ] = connect.now ()

	table = r.db ('supplements').table ("inventory");

	table.index_create (
		"product_name",
		r.row ["struct_2"] ["product"] ["name"]
	).run (c)
	
	table.index_wait ().run (c);