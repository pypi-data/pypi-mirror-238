
'''
import cyte.hygiene.__stem.start as start_stem
stem = start_stem.presently ()
stem.stop ()
'''

import pathlib

import cyte.hygiene._system.start as hygiene_start
import cyte.hygiene._system.connect as connect

import cyte.hygiene.__stem.climate as stem_climate

def presently (
	rethink_params = []
):
	stem_climate.change ()
	
	print ("rethink_params:", rethink_params)
	
	ly = hygiene_start.now (
		process = {
			"cwd": pathlib.Path (__file__).parent.resolve ()
		},
		rethink_params = rethink_params
	)
	
	#
	#	https://rethinkdb.com/api/python/wait
	#
	
	[ r, c ] = connect.now ()
	r.db ('foods').table ('inventory').wait ().run (c)
	r.db ('supplements').table ('inventory').wait ().run (c)


	return ly