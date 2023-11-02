



'''
import warehouses.supplements.clique as supplements
supplements.clique ()
'''
import warehouses.supplements.inventory.clique as supplements_inventory

def clique ():

	import click
	@click.group ("supplements")
	def group ():
		pass

	
	group.add_command (supplements_inventory.clique ())

	return group