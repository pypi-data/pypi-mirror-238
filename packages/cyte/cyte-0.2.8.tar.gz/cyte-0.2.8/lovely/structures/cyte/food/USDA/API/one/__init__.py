



'''
import cyte.food.USDA.API.one as USDA_food_API
food = USDA_food_API.find (
	1960255,
	API_ellipse = "",
	kind = "branded"
)

food_data = food ["data"]
food_source = food ["source"]
'''

'''
	curl https://api.nal.usda.gov/fdc/v1/food/1960255?api_key=DEMO_KEY
'''

import json
import requests

import cyte.food.USDA.API.one.assertions.branded as assertions_branded
import cyte.food.USDA.API.one.assertions.foundational as assertions_foundational
import cyte.food.USDA.API.one.source as USDA_API_source


def find (
	FDC_ID,
	API_ellipse = "",
	kind = "branded"
):
	host = 'https://api.nal.usda.gov'
	path = f'/fdc/v1/food/{ FDC_ID }'
	params = f'?api_key={ API_ellipse }'
	
	address = host + path + params
	
	print (
		"The request is on track to be sent.", 
		json.dumps ({ "address": address }, indent = 2)
	)

	r = requests.get (address)
	print ("This response code was received.", r.status_code)
	
	data = json.loads (r.text)

	if (kind == "branded"):
		assertions_branded.run (data)
		
	elif (kind == "foundational"):
		assertions_foundational.run (data)

	return {
		"data": data,
		"source": USDA_API_source.find (FDC_ID)
	}