

'''
	./produce warehouse foods inventory 
'''
def clique ():

	import click
	@click.group ("inventory")
	def group ():
		pass


	'''
		./produce foods inventory insert-doc --fdc-id 1960255
	'''
	@group.command ("insert-doc")
	@click.option ('--fdc-id', required = True)
	def add (fdc_id):
		import warehouses.foods.inventory.doc.insert as insert_food
		insert_food.now (fdc_id)
			

	
		return;
		
	'''
		./produce foods inventory find --fdc-id 1960255
	'''
	@group.command ("find")
	@click.option ('--fdc-id', required = True)
	def find (fdc_id):
		print ('FIND')
	
		return;

	return group