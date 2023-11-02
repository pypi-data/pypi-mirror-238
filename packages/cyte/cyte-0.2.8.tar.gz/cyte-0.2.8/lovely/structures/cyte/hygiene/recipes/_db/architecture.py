

import cyte.hygiene.recipes._db.create as create_recipes_db
import cyte.hygiene.recipes.inventory._table.create as create_recipes_inventory_table

def create ():
	create_recipes_db.hastily ()
	create_recipes_inventory_table.hastily ()

	return;