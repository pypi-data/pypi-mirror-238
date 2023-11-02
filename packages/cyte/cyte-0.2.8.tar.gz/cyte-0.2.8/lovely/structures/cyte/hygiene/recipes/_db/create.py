
'''
import cyte.hygiene.recipes._db.create as create_recipes_db
import cyte.hygiene.recipes.inventory._table.create as create_recipes_inventory_table

create_recipes_db.hastily ()
create_recipes_inventory_table.hastily ()
'''
import cyte.hygiene._system.connect as connect

def hastily ():
	table = "recipes"

	[ r, c ] = connect.now ()
	returns = r.db_create (table).run (c)
	
	db_list = r.db_list ().run (c)
	assert (table in db_list)

	return;