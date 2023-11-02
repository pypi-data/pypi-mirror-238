


'''
import pathlib
import cyte.hygiene._system.start as hygiene_start
ly = hygiene_start.now (
	process = {
		"cwd": pathlib.Path (__file__).parent.resolve ()
	},
	rethinkdb = [
		f"--pid-file {}"
	],
	wait = True
)

# ly.process.wait ()

ly.stop ()
'''

'''
	steps:
		check to make sure can't connect
'''

'''
setsid
'''

import subprocess
import shlex

import cyte.hygiene._system.climate as climate
import cyte.hygiene._system.cannot_connect as cannot_connect

def now (
	rethink_params = [],
	** keywords
):
	#
	#	check if can connect,
	#	if it can, then there's already a rethinkdb process
	#	running
	#
	cannot_connect.ensure (
		loops = 2
	)

	# ports = params ["ports"]
	process_keys = keywords ["process"]
	
	if ("wait" in keywords):
		wait = keywords ["wait"]
	else:
		wait = False

	ports = climate.find ("ports")
	driver_port = str (ports ["driver"])
	cluster_port = str (ports ["cluster"])
	http_port = str (ports ["http"])

	script = " ".join ([
		"rethinkdb",
		f"--driver-port { driver_port }",
		f"--cluster-port { cluster_port }",
		f"--http-port { http_port }",
		
		* rethink_params
	])
	
	
	print ("script:", script)
	print ("rethink_params:", rethink_params)
	print ("keywords:", keywords)

	
	class ly:
		def __init__ (this, script):
			this.script = script;
			this.process = subprocess.Popen (
				shlex.split (script),
				** process_keys
			)
			
			print ("this.process:", this.process)

		def stop (this):
			print ('stopping rethinkdb')
		
			this.process.kill ()

	lymphatic = ly (script)

	
	return lymphatic