

'''
import warehouses.foods.clique as foods
foods.clique ()
'''
import warehouses.foods.inventory.clique as foods_inventory

def clique ():

	import click
	@click.group ("foods")
	def group ():
		pass

	
	group.add_command (foods_inventory.clique ())
	#foods_inventory.clique (group)

	return group