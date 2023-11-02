

'''
	import cyte.hygiene._system.connect as connect
	[ r, c ] = connect.start ()
'''

'''
	[ r, c ] = connect.now (
		connect.parameters (
			loops = 5
		)
	)
'''


from rethinkdb import RethinkDB
import cyte.hygiene._system.climate as climate
import botanical.cycle as cycle


class parameters:
	def __init__ (this, ** keywords):
		print ("keywords:", keywords)
	
		if ("loops" in keywords):
			this.loops = keywords ['loops']
		else:
			this.loops = 10
		
		this.delay = 1
		


def now (
	params = parameters ()
):
	print ("params:", params)

	connection_attempt = 1;
	def connect (* positionals, ** keywords):
		ports = climate.find ("ports")
		driver_port = ports ["driver"]
	
		nonlocal connection_attempt;
		print (
			f"Attempting rethink connection on port: { driver_port }, attempt", 	
			connection_attempt
		)
		
		connection_attempt += 1
	
		
		
		r = RethinkDB ()
		
		'''	
			conn = r.connect (
				host = 'localhost',
				port = 28015,
				ssl = {
					'ca_certs': '/path/to/ca.crt'
				}
			)
		'''
		c = r.connect (
			host = 'localhost',
			port = driver_port
		)

		# ®©
		return [ r, c ];
			
	connection = cycle.loops (
		connect, 
		cycle.presents ([]),
		
		loops = params.loops,
		delay = params.delay
	)
	
	return connection;
	
	
start = now