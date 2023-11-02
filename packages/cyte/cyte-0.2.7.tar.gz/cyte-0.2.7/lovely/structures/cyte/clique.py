
from cyte.structs.CLIQUE import structs_CLIQUE

def START ():
	import click
	@click.group ()
	def GROUP ():
		pass


	import click
	@click.command ("example")
	def EXAMPLE ():	
		print ("EXAMPLE")

		return;
	GROUP.add_command (EXAMPLE)


	structs_CLIQUE (GROUP)


	GROUP ()


START ()

#
