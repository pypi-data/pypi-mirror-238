
'''
import cyte.hygiene.foods.inventory.doc.get as get_food
food = get_food.now (1)
'''
import cyte.hygiene._system.connect as connect

def now (emblem):
	[ r, c ] = connect.now ()

	db = "foods"
	table = "inventory"
	primary_key = "emblem"
	returns = r.db (db).table (table).get (emblem).pluck ('struct_2', 'sources', 'emblem').run (c)

	return returns