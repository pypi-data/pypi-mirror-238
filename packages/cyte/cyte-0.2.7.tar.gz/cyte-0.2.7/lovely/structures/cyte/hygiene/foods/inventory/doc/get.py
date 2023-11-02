
'''
import warehouses.foods.inventory.doc.get as get_food
food = get_food.now (1)
'''

def now (emblem):
	[ r, c ] = connect.now ()

	db = "foods"
	table = "inventory"
	primary_key = "emblem"
	returns = r.db (db).table (table).get (emblem)

	return returns