

'''
	caution, allows users to input a regex expression???
'''


'''
import cyte.hygiene._aggregates.search as search
returns = search.start ({
	"product name": "",
	"limit": 10
})
alarm = returns ["alarm"]

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

	def pluck_and_filter (table):
		return table.order_by ( index = 'product_name' ).filter (
			lambda product :		
			product ['struct_2'] ['product'] ['name'].downcase ().match (product_name)
		).pluck (
			'struct_2',
			'emblem',
			'sources'
		)
		
	foods_discovery = pluck_and_filter (foods_table)
	supps_discovery = pluck_and_filter (supps_table)


	foods = foods_discovery.run (c)
	supps = supps_discovery.run (c)


	def next_document (selector):
		try:
			return selector.next ()
		except Exception as E:
			return False
		
	def product_name (product):
		try:
			return product ["struct_2"]['product']['name']
		except Exception as E:
			return ""

	food_matches = foods_discovery.count ().run (c)
	supp_matches = supps_discovery.count ().run (c)
	foods_index = 0
	supps_index = 0	
	
	print ("food_matches:", food_matches)
	print ("supp_matches:", supp_matches)
	
	food = next_document (foods)
	supp = next_document (supps)
	
	last_food_emblem = ""
	last_supp_emblem = ""
	
	found = []
	
	
	
	place = 1
	while (place <= limit):
		#print (place, type (food), type (supp))
	
		if (type (food) == dict):
			if (type (supp) == dict):
				# there are more food and supplements
				
				if (product_name (supp) < product_name (food)):
					found.append (supp)
					last_supp_emblem = supp ['emblem']
					
					supp = next_document (supps)					
				else:				
					found.append (food)
					last_food_emblem = food ['emblem']
					
					food = next_document (foods)
					
				
			else:
				# there are more foods, and no more supplements
				found.append (food)
				last_food_emblem = food ['emblem']
				
				food = next_document (foods)
				
		else:
			# there are no more foods
			
			if (type (supp) == dict):
				# there are more supplements, and no more foods
				found.append (supp)
				last_supp_emblem = supp ['emblem']
				
				supp = next_document (supps)
				
			else:
				# there are no more food or supplements
				
				break;

		place += 1
		
	print ("?")


	return {
		"alarm": "",
		
		"products": found,
		"last food": last_food_emblem,
		"last supp": last_supp_emblem		
	} 

