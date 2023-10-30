

'''
	if servings size length is > 1,
	
		246811
			this one the second serving size is listed
			in volume.... so impossible to do calculations
			on.
	
		presumably the ingredients will all use one
		of the serving sizes.....
		
		however, 
'''

import cyte.integer.STRING_IS_integer as STRING_IS_integer

def calc (
	NIH_supplement_data,
	NIH_supplement_data_struct_2
):
	assert ("netContents" in NIH_supplement_data)
	net_contents = NIH_supplement_data ["netContents"]

	assert ("servingSizes" in NIH_supplement_data)
	serving_sizes = NIH_supplement_data ["servingSizes"]

	assert ("servingsPerContainer" in NIH_supplement_data)
	servings_per_container = NIH_supplement_data ["servingsPerContainer"]

	#
	#	examples: chia_seeds_214893
	#
	if (NIH_supplement_data_struct_2 ["form"]["unit"] == "gram"):
		if (
			len (serving_sizes) == 1 and
			STRING_IS_integer.CHECK (servings_per_container) and
			serving_sizes [0] ["minQuantity"] == serving_sizes [0] ["maxQuantity"]
		):
			return serving_sizes [0] ["maxQuantity"] 

	if (
		len (net_contents) == 1 and
		len (serving_sizes) == 1 and
		STRING_IS_integer.CHECK (servings_per_container) and
		serving_sizes [0] ["minQuantity"] == serving_sizes [0] ["maxQuantity"] and
		net_contents [0] ["quantity"] / int (servings_per_container) == serving_sizes [0] ["maxQuantity"]
	):
		return serving_sizes [0] ["maxQuantity"]
		
	raise Exception ("The defined serving size of the supplement could not be calculated.")
		

	#
	#	This is necessary for composition calculations,
	#	but recommendations should be determined elsewhere.
	#
	#	if:
	#		len (netContents)  == 1 and
	#
	#		import cyte.integer.STRING_IS_integer as STRING_IS_integer
	#		STRING_IS_integer.CHECK (servingsPerContainer)
	#
	#		len (servingSizes) == 1
	#
	#		servingSizes [0].minQuantity == servingSizes[0].maxQuantity
	#
	#		netContents [0].quantity / int (servingsPerContainer) == servingSizes[0].maxQuantity
	#
	#	then:
	#		"quantity" = servingSizes[0].maxQuantity
	#		"quantity" = 3
	#
	


	return;