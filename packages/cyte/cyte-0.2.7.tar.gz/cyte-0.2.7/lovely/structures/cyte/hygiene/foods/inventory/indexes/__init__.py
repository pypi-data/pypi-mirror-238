
'''
import cyte.hygiene.foods.inventory.indexes as foods_indexes

'''
import cyte.hygiene._system.connect as connect

def create ():
	[ r, c ] = connect.now ()

	foods_table = r.db ('foods').table ("inventory");

	foods_table.index_create (
		"product_name",
		r.row ["struct_2"] ["product"] ["name"]
	).run (c)
	
	foods_table.index_wait ().run (c);