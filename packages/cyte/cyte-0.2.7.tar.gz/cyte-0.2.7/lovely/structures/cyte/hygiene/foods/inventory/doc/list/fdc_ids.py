
'''
import cyte.hygiene.foods.inventory.doc.list.fdc_ids as fdc_id_list
fdc_ids = fdc_id_list.find ()
'''

import cyte.hygiene._system.connect as connect
import cyte.hygiene.__stem.climate as stem_climate

def find ():
	[ r, c ] = connect.now ()

	ids = r.db ('foods').table ('inventory').pluck ({ 
		'struct_2': { "product": [ "FDC ID" ] }
	}).map (
		lambda document :
		document ['struct_2'] ['product']['FDC ID']
	).run (c)
	
	return list (ids)
	
	cursor = r.db ('foods').table ('inventory').pluck ({ 
		'struct_2': { "product": [ "FDC ID" ] }
	}).run (c)
	
	ids = list (cursor)
	
	
	def fn (document):
		return document ["struct_2"]["product"]["FDC ID"]
	
	return list (map (
		fn,
		ids
	))
