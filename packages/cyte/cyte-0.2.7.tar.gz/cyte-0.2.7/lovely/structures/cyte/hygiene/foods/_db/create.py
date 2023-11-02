
'''
import cyte.hygiene.foods._db.create as create_foods_db
import cyte.hygiene.foods.inventory.table.create as create_foods_inventory_table

create_foods_db.hastily ()
create_foods_inventory_table.hastily ()
'''
import cyte.hygiene._system.connect as connect

def hastily ():
	[ r, c ] = connect.now ()
	returns = r.db_create ('foods').run (c)
	
	db_list = r.db_list ().run (c)
	assert ("foods"	in db_list)

	return;