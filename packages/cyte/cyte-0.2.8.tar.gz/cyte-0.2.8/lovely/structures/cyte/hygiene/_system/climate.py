


'''
import cyte.hygiene._system.climate as climate
climate.change ("ports", {
	"driver": 18871,
	"cluster": 0,
	"http": 0	
})
'''

'''
import cyte.hygiene._system.climate as climate
ports = climate.find ("ports")
'''

import copy

climate = {
	"ports": {
		"driver": 18871,
		"cluster": 0,
		"http": 0
	}
}

def change (field, plant):
	#global CLIMATE;
	climate [ field ] = plant


def find (field):
	return copy.deepcopy (climate) [ field ]