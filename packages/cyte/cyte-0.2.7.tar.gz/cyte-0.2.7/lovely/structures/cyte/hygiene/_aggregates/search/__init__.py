

'''
	caution, allows users to input a regex expression???
'''


'''
import cyte.hygiene._aggregates.search as search
search.start ({
	"product name": "",
	"limit": 10
})
'''

'''
	struct_2: {
		product: {
			name: ""
		}
	}
'''

'''
	get the first 3 products,
	where the name includes: "s"
'''

'''
	possibilities:
		# https://rethinkdb.com/api/javascript/map/#wrapper
		r.table('heroes').map(r.table('villains'), function (hero, villain) {
			return hero.merge({villain: villain});
		}).run(conn, callback);
'''

import cyte.hygiene._doc.string.valid_characters as validate_characters

import cyte.hygiene._system.connect as connect

def start (
	presents,
	
	records = 0
):
	[ r, c ] = connect.start ()
	
	try:
		product_name = ""
		if ("product name" in presents):
			product_name = presents ["product name"].lower ()
			valid = validate_characters.start (product_name)		
			
			if (not valid):		
				return {
					"alarm": "The search literature contains unsearchable characters",
					"products": []
				}
	except Exception as E:
		print ("Exception:", E)
	
		return {
			"alarm": "An exception occurred while attempting to parse the search literature.",
			"products": []
		}
		
	limit = 10
	if ("limit" in presents and type (presents['limit']) == int):	
		limit = presents ['limit']
		
	foods_table = r.db ('foods').table ('inventory');
	supps_table = r.db ('supplements').table ('inventory');

	foods_discovery = foods_table.order_by ( index = 'product_name' ).map (
		lambda product :
		product ['struct_2']
	).filter (
		lambda product :		
		product ['product'] ['name'].downcase ().match (product_name)
	)
	supps_discovery = supps_table.order_by ( index = 'product_name' ).map (
		lambda product :
		product ['struct_2']
	).filter (
		lambda product :		
		product ['product'] ['name'].downcase ().match (product_name)
	)

	foods = foods_discovery.run (c)
	supps = supps_discovery.run (c)



	def next_document (selector):
		try:
			return selector.next ()
		except Exception as E:
			return False
		

	food_matches = foods_discovery.count ().run (c)
	supp_matches = supps_discovery.count ().run (c)
	foods_index = 0
	supps_index = 0	
	
	print ("food_matches:", food_matches)
	print ("supp_matches:", supp_matches)
	
	food = next_document (foods)
	supp = next_document (supps)
	
	found = []
	
	place = 1
	while (place <= limit):
		#print (place, type (food), type (supp))
	
		if (type (food) == dict):
			if (type (supp) == dict):
				# there are more food and supplements
				
				if (supp ['product']['name'].lower () < food ['product']['name'].lower ()):
					if (records >= 1):
						print ("adding supp", {
							"supp": supp ['product']['name'].lower (),
							"food": food ['product']['name'].lower ()
						})
				
					found.append (supp)
					supp = next_document (supps)					
				else:
					if (records >= 1):
						print ("adding food", {
							"supp": supp ['product']['name'].lower (),
							"food": food ['product']['name'].lower ()
						})
					
					found.append (food)
					food = next_document (foods)
					
				
			else:
				# there are more foods, and no more supplements
				found.append (food)
				food = next_document (foods)
				
		else:
			# there are no more foods
			
			if (type (supp) == dict):
				# there are more supplements, and no more foods
				found.append (supp)
				supp = next_document (supps)
				
			else:
				# there are no more food or supplements
				
				break;

		place += 1
		
	print ("?")


	return {
		"products": found
	} 

