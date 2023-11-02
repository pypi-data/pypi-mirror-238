


def find_grams_quantity (net_contents):
	for net_content in net_contents:
		if (net_content ["unit"] == "Gram(s)"):
			return net_content ["quantity"]

	raise Exception (f"Quantity of grams could not be found in net_contents { net_contents }")
	

def calc_QUANTITY (
	NIH_supplement_data,
	NIH_supplement_data_struct_2
):
	assert ("netContents" in NIH_supplement_data)
	net_contents = NIH_supplement_data ["netContents"]
	
	if (NIH_supplement_data_struct_2 ["form"]["unit"] == "gram"):
		return find_grams_quantity (
			net_contents
		)
	
	if (
		len (net_contents) == 1
	):
		return net_contents [0] ["quantity"]
		
	raise Exception ("The form quantity of the supplement could not be calculated.")
