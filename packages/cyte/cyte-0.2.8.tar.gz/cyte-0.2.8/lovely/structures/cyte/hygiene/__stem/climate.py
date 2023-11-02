
'''
import cyte.hygiene.__stem.climate as stem_climate
stem_climate.change ()
'''

import cyte.hygiene._system.climate as climate

def change ():
	climate.change ("ports", {
		"driver": 57345,
		"cluster": 57346,
		"http": 57347
	})