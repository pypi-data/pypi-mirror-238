

def grams_in_net_contents (net_contents):
	for net_content in net_contents:
		if (net_content ["unit"] == "Gram(s)"):
			return True

	return False


def calc (nih_supplement_data):
	assert ("netContents" in nih_supplement_data)
	net_contents = nih_supplement_data ["netContents"]

	assert ("physicalState" in nih_supplement_data)
	physical_state = nih_supplement_data ["physicalState"]

	assert ("servingSizes" in nih_supplement_data)
	serving_sizes = nih_supplement_data ["servingSizes"]

	if (
		physical_state ["langualCodeDescription"] == "Other (e.g. tea bag)" and
		grams_in_net_contents (net_contents) and 
		len (serving_sizes) == 1 and
		serving_sizes [0] ["unit"] == "Gram(s)"
	):
		#
		#	the form is 1 gram
		#
		return "gram"

	if (
		len (net_contents) == 1 and
		net_contents [0] ["unit"] == "Vegan Cap(s)" and 
		physical_state ["langualCodeDescription"] == "Capsule" and
		len (serving_sizes) == 1 and
		serving_sizes [0] ["unit"] == "Capsule(s)"
	):
		return "Vegan Capsule"

	if (
		len (net_contents) == 1 and
		net_contents [0] ["unit"] == "Tablet(s)" and 
		physical_state ["langualCodeDescription"] == "Tablet or Pill" and
		len (serving_sizes) == 1 and
		serving_sizes [0] ["unit"] == "Tablet(s)"
	):
		return "Tablet"
		
	if (
		len (net_contents) == 1 and
		net_contents [0] ["unit"] == "Coated Tablet(s)" and 
		physical_state ["langualCodeDescription"] == "Tablet or Pill" and
		len (serving_sizes) == 1 and
		serving_sizes [0] ["unit"] == "Tablet(s)"
	):
		return "Coated Tablet"
		
	raise Exception ("The form unit of the supplement could not be calculated.")