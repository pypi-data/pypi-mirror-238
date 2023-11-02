
'''
	warning:
		this is actually supposed to be given server access
'''

'''
	

	import cyte.hygiene._aggregates.recipes as aggregate_recipe
	recipe = aggregate_recipe.calc (
		foods = [ '2449699', '2138281', '2548008' ],
		supplements = [ '2261967', '214893' ]
	)
	
	recipe_struct_grove = recipe.recipe_struct_grove
'''

import cyte.recipes.struct_2 as struct_2_recipes
import cyte.structs.DB.access as access
import cyte.structs.scan.trees_form_1 as trees_form_1

import cyte.hygiene._system.connect as connect


def calc (
	foods = [],
	supplements = []
):
	[ r, c ] = connect.now ()

	foods_cursor = r.db ('foods').table ('inventory').filter (
		lambda document : 
		r.expr (foods).contains (document [ 'struct_2' ]['product']['FDC ID'])
	).map (
		lambda document :
		document [ 'struct_2' ]
	).run (c)
	foods_list = list (foods_cursor) 

	import json
	print (json.dumps (foods_list, indent = 4))

	supplements_cursor = r.db ('supplements').table ('inventory').filter (
		lambda document : 
		r.expr (supplements).contains (document [ 'struct_2' ]['product']['DSLD ID'])
	).map (
		lambda document :
		document [ 'struct_2' ]
	).run (c)
	supplements_list = list (supplements_cursor) 

	recipe = struct_2_recipes.calc ({
		"products": [
			* foods_list,
			* supplements_list
		],
		"structs grove": trees_form_1.start (access.DB ())
	})
	
	print (recipe)
	
	#recipe_struct_grove = recipe.recipe_struct_grove;
	
	return recipe