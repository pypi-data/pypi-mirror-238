

'''
import cyte.hygiene.foods.inventory._table.create as create_foods_inventory_table
'''

import cyte.hygiene._system.connect as connect

import cyte.hygiene.foods.inventory.indexes as foods_indexes

def hastily ():
	primary_key = "emblem"
	table = "inventory"
	db = "foods"

	[ r, c ] = connect.now ()
	returns = r.db (db).table_create (
		table,
		primary_key = primary_key
	).run (c)
	
	print ("returns:", returns)

	table_list = r.db (db).table_list ().run (c)
	assert (table	in table_list)

	config = r.db (db).table (table).config (c)
	assert (config ["primary_key"] == primary_key)

	foods_indexes.create ()
	


	return;