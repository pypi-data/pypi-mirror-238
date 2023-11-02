



'''
	python3 status.py "supplements/NIH/struct_2/_status_coated_tablets/STATUS_DEVA_multivitamin_276336.py"
'''

'''
https://www.amazon.com/Deva-Vegan-Vitamins-Multivitamin-Supplement/dp/B01FRJTSW4
'''


'''
https://dsld.od.nih.gov/label/276336
'''

import json

import cyte.supplements.NIH.examples as NIH_examples
import cyte.supplements.NIH.struct_2 as struct_2

def CHECK_1 ():
	supplement_struct_2 = struct_2.calc (
		NIH_examples.RETRIEVE ("coated tablets/multivitamin_276336.JSON")
	)
	
	#import pyjsonviewer
	#pyjsonviewer.view_data (json_data = supplement_struct_2)
	
	#print ("supplement_struct_2:", json.dumps (supplement_struct_2, indent = 4))
	#print (supplement_struct_2 ["product"])

	assert (supplement_struct_2 ["product"]["name"] == "Vegan Multivitamin & Mineral Supplement with Greens")
	assert (supplement_struct_2 ["product"]["DSLD ID"] == "276336")
	
	assert (supplement_struct_2 ["brand"]["name"] == "DEVA")
	assert (
		supplement_struct_2 ["defined"]["serving size"] ==
		{
			"quantity": 1
		}
	)
	
	assert (supplement_struct_2 ["form"]["unit"] == "Coated Tablet")
	assert (supplement_struct_2 ["form"]["quantity"] == "90")

	#print ("supplement_struct_2 IQ:", len (supplement_struct_2 ["ingredients"]["quantified"]))
	assert (
		len (supplement_struct_2 ["ingredients"]["quantified grove"]) == 31
	),len (supplement_struct_2 ["ingredients"]["quantified grove"])

	#print ("supplement_struct_2 IU:", len (supplement_struct_2 ["ingredients"]["unquantified"]))
	assert (len (supplement_struct_2 ["ingredients"]["unquantified"]) == 7) 

	from os.path import dirname, join, normpath
	import sys
	import pathlib
	import cyte._sculpt as sculpt
	sculpt.start (
		normpath (join (pathlib.Path (__file__).parent.resolve (), "struct_2_multivitamin_276336.json")),
		json.dumps (supplement_struct_2, indent = 4)
	)


checks = {
	"DEVA multivitamin 276336": CHECK_1
}












#