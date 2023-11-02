
'''
import cyte.hygiene.foods._db.architecture as foods_architecture
foods_architecture.create ()
'''
import cyte.hygiene.foods._db.create as create_foods_db
import cyte.hygiene.foods.inventory._table.create as create_foods_inventory_table

def create ():
	create_foods_db.hastily ()
	create_foods_inventory_table.hastily ()
	
	

	return;