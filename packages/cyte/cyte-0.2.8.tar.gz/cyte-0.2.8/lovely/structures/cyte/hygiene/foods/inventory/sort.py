



'''

data explorer:
	doesn't work:
		 r.db ('foods').table ("inventory").indexDrop ('product_name');
		 
		 r.db ('foods').table ("inventory").indexCreate (
			"product_name",
			r.row ("struct_2") ("product") ("name")
		)
	
		r.db ('foods').table ("inventory").orderBy ({ index: 'product_name' }).map (
			function (product) {
				return product ('struct_2') ('product')('name')
			}
		) 
'''

'''
	foods_table = r.db ('foods').table ("inventory")
	
	foods = foods_table.order_by ( index = 'product_name' ).map (
		lambda product :
		product ['struct_2'] ['product'] ['name' ]
	).run (c)
'''