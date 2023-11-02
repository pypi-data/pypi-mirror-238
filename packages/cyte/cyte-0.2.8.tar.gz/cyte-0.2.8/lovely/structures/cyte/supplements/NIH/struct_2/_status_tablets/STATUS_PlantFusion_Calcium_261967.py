



'''
	python3 status.py "supplements/NIH/struct_2/_status_tablets/STATUS_PlantFusion_Calcium_261967.py"
'''

'''
	https://www.amazon.com/PlantFusion-Supports-Mineralized-Supplement-90/dp/B07VP749CF
'''

import json

import cyte.supplements.NIH.examples as NIH_examples
import cyte.supplements.NIH.struct_2 as struct_2

import cyte._ensure.eq as equality

def CHECK_1 ():
	supplement_struct_2 = struct_2.calc (NIH_examples.RETRIEVE ("tablets/calcium_261967.JSON"))
	
	from os.path import dirname, join, normpath
	import sys
	import pathlib
	import cyte._sculpt as sculpt
	sculpt.start (
		normpath (join (pathlib.Path (__file__).parent.resolve (), "struct_2_calcium_261967.json")),
		json.dumps (supplement_struct_2, indent = 4)
	)
	
	#print ("supplement_struct_2:", json.dumps (supplement_struct_2, indent = 4))
	
	assert (supplement_struct_2 ["product"]["name"] == "Vegan Plant-Based Calcium 1,000 mg")
	assert (supplement_struct_2 ["product"]["DSLD ID"] == "261967")

	
	assert ("brand" in supplement_struct_2)
	assert ("name" in supplement_struct_2 ["brand"])
	assert (type (supplement_struct_2 ["brand"]["name"]) == str)
	
	assert (
		supplement_struct_2 ["defined"]["serving size"] ==
		{
			"quantity": 3
		}
	), supplement_struct_2 ["defined"]
	assert (
		supplement_struct_2 ["defined"]["servings per container"] ==
		'30'
	), supplement_struct_2 ["defined"]
	
	
	assert (supplement_struct_2 ["form"]["unit"] == "Tablet"), supplement_struct_2 ["form"]
	assert (supplement_struct_2 ["form"]["quantity"] == "90"), supplement_struct_2 ["form"]
	

	
	equality.check (len (supplement_struct_2 ["ingredients"]["quantified grove"]), 9)

	equality.check (
		supplement_struct_2 ["ingredients"]["quantified grove"][7]["name"],
		"Vitamin D3"
	)
	
	
	assert (
		supplement_struct_2 ["ingredients"]["quantified grove"][7]["quantity"]["per form"]["listed"] ==
		{
			"fraction string": "20/3",
			'float string': '6.666666666666667',
			"unit": "mcg"
		}
	), supplement_struct_2 ["ingredients"]["quantified grove"][7]["quantity"]["per form"]
	
	
	equality.check (
		supplement_struct_2 ["ingredients"]["quantified grove"][7]["mass"]["per form"]["fraction string grams"],
		"1/150000"
	)
	
	assert (
		supplement_struct_2 ["ingredients"]["quantified grove"][7]["mass"]["per package"]["fraction string grams"] ==
		"3/5000"
	), supplement_struct_2 ["ingredients"]["quantified grove"][7]

	
	assert (len (supplement_struct_2 ["ingredients"]["unquantified"]) == 4)

	equality.check (
		supplement_struct_2 ["mass"] ["sum of quantified ingredients, exluding effectual"]["per package"]["fraction string grams"],
		"580153/375000"
	)
	equality.check (
		supplement_struct_2 ["mass"]  ["sum of quantified ingredients, exluding effectual"]["per form"]["fraction string grams"],
		"580153/33750000"
	)
	
	#import pyjsonviewer
	#pyjsonviewer.view_data (json_data = supplement_struct_2)
	
	
	
	
	
checks = {
	"calcium 261967": CHECK_1
}