

'''
import cyte.hygiene.supplements.inventory.doc.insert as insert_supplements
insert_supplements.now ({
	"dsld_id": 261967,
	"api_key": api_key,
	
	"insert": "yes"
})
'''


import cyte.hygiene._system.connect as connect	
	
import json

def now (params):
	if ("dsld_id" in params):
		dsld_id = str (params ["dsld_id"])
	else:
		raise Exception ("The dsld_id was not found.")

	if ("api_key" in params):
		api_key = params ["api_key"]
	else:
		raise Exception ("The api_key was not found.")
		
	insert = "no"
	if ("insert" in params):
		insert = params ["insert"]	
		
	[ r, c ] = connect.now ()
	db = "supplements"
	table = "inventory"
	primary_key = "emblem"
	
	already_inserted = r.db (db).table (table).filter (
		lambda doc : doc ["struct_2"]["product"]["DSLD ID"] == dsld_id
	).count ().run (c)
	if (already_inserted >= 1):
		print (f"dsld_id { dsld_id } is already in the table.")
		return;


	import cyte.supplements.NIH.API.one as NIH_API_one
	supplement = NIH_API_one.find (
		dsld_id,
		api_key
	)
	
	NIH_supplement_data = supplement ["data"]
	NIH_supplement_source = supplement ["source"]
	
	import cyte.supplements.NIH.struct_2 as struct_2
	supplement_struct_2 = struct_2.calc (NIH_supplement_data)

	document = {
		"struct_2": supplement_struct_2,
		"NIH supplement data": NIH_supplement_data,
		"sources": {
			"NIH": NIH_supplement_source
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
		
	return {
		"document": document
	}