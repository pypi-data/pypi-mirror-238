



'''
import cyte.hygiene.supplements._db.create as create_supplements_db
import cyte.hygiene.supplements.inventory.table.create as create_supplements_inventory_table

create_supplements_db.hastily ()
create_supplements_inventory_table.hastily ()
'''
import cyte.hygiene._system.connect as connect

def hastily ():
	[ r, c ] = connect.now ()
	returns = r.db_create ('supplements').run (c)
	
	db_list = r.db_list ().run (c)
	assert ("supplements"	in db_list)

	return;