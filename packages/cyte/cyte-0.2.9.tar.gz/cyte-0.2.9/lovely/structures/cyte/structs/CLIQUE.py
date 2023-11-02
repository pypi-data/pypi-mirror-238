

'''
	plan:
		cyte structs 
		
'''

from cyte.structs.scan.CLIQUE import structs_scan_CLIQUE

def structs_CLIQUE (GROUP):

	import click
	@GROUP.group ("structs")
	def GROUP ():
		pass
		
	import click
	@GROUP.command ("find")
	def find ():	



		return;
		
		
	structs_scan_CLIQUE (GROUP)	

	return;