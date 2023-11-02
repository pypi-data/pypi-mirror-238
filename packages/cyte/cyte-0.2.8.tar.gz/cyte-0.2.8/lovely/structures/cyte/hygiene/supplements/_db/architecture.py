
'''
import cyte.hygiene.supplements._db.architecture as supplements_architecture
supplements_architecture.create ()
'''
import cyte.hygiene.supplements._db.create as create_supplements_db
import cyte.hygiene.supplements.inventory._table.create as create_supplements_inventory_table

def create ():
	create_supplements_db.hastily ()
	create_supplements_inventory_table.hastily ()
	

	return;