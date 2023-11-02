

'''
	./produce warehouse supplements inventory 
'''
def clique ():

	import click
	@click.group ("inventory")
	def group ():
		pass


	'''
		./produce supplements inventory insert-doc --dsld-id 261967
	'''
	@group.command ("insert-doc")
	@click.option ('--dsld-id', required = True)
	def add (dsld_id):
		import warehouses.supplements.inventory.doc.insert as insert_food
		insert_food.now (dsld_id)
			

	
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