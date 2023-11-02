



def structs_scan_CLIQUE (GROUP):

	import click
	@GROUP.group ("scan")
	def GROUP ():
		pass
	
	'''
		./cyte_dev structs scan struct-find 
	'''
	import click
	@GROUP.command ("struct-find")
	def struct_find ():	
		print ("struct find")


		return;
		

	return;