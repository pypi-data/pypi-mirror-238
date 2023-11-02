
'''
	import cyte.hygiene.foods.inventory.doc.insert as insert_food
	insert_food.now ({
		"fdc_id": 1960255,
		"api_key": USDA_api_key,
		"insert": "yes"
	})
	
	
	plan:
		insert_food.now ({
			"document": {
				"struct_2": food_struct_2,
				"USDA food data": USDA_food_data,
				"sources": {
					"USDA": USDA_food_source
				}
			}
		})
'''


import cyte.hygiene._system.connect as connect
	
import json

def now (params):
	if ("fdc_id" in params):
		fdc_id = str (params ["fdc_id"])
	else:
		raise Exception ("The fdc_id was not found.")

	if ("api_key" in params):
		api_key = params ["api_key"]
	else:
		raise Exception ("The api_key was not found.")

	insert = "no"
	if ("insert" in params):
		insert = params ["insert"]

	[ r, c ] = connect.now ()
	db = "foods"
	table = "inventory"
	primary_key = "emblem"
	
	already_inserted = r.db (db).table (table).filter (
		lambda doc : doc ["struct_2"]["product"]["FDC ID"] == fdc_id
	).count ().run (c)
	if (already_inserted >= 1):
		raise Exception (f"fdc_id { fdc_id } is already in the table.")
		return

	import cyte.food.USDA.API.one as USDA_food_API
	food = USDA_food_API.find (
		fdc_id,
		API_ellipse = api_key,
		kind = "branded"
	)

	USDA_food_data = food ["data"]
	USDA_food_source = food ["source"]
	
	import cyte.food.USDA.struct_2 as USDA_struct_2
	food_struct_2 = USDA_struct_2.calc (USDA_food_data)

	print (json.dumps (food_struct_2, indent = 4))
	
	document = {
		"struct_2": food_struct_2,
		"USDA food data": USDA_food_data,
		"sources": {
			"USDA": USDA_food_source
		}
	}	
	
	if (insert == "yes"):
		returns = r.db (db).table (table).insert ({		
			primary_key: (
				r.branch (
					r.db (db).table (table).count () == 0,
					1,
					r.expr (
						r.db (db).table (table).max (primary_key).get_field (
							primary_key
						).coerce_to ('number')
					).add (1)
				)
			),
			** document
		}).run (c)

		print ("returns:", returns)

		return {
			"document": document,
			"insertion": returns
		}
		
	print ('"insert": "yes" not designated, returning the document')
		
	return {
		"document": document
	} 