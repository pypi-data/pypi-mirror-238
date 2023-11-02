


'''
import cyte.hygiene.supplements.inventory.list.dsld_id as dsld_id_list
dsld_id_lists = dsld_id_list.find ()
'''

import cyte.hygiene._system.connect as connect
import cyte.hygiene.__stem.climate as stem_climate

def find ():
	[ r, c ] = connect.now ()

	db = 'supplements'
	table = 'inventory'

	ids = r.db (db).table (table).pluck ({ 
		'struct_2': { "product": [ "DSLD ID" ] }
	}).map (
		lambda document :
		document ['struct_2'] ['product'] ['DSLD ID']
	).run (c)
	
	return list (ids)
	
	cursor = r.db (db).table (table).pluck ({ 
		'struct_2': { "product": [ "DSLD ID" ] }
	}).run (c)
	
	ids = list (cursor)
	
	
	def fn (document):
		return document ["struct_2"] ["product"] ["FDC ID"]
	
	return list (map (
		fn,
		ids
	))
