
'''
	python3 STATUS.py "structs/scan/names/contains_substring/STATUS_DYNAMIC_1.py"
'''

import cyte.structs.DB.access as access
import cyte.structs.scan.names.contains_substring as structs_WHERE_name_CONTAINS_SUBSTRING

def CHECK_1 ():	
	structs = structs_WHERE_name_CONTAINS_SUBSTRING.find (
		access.DB (),
		"VITAMIN B"
	)
	structs_VAR_CAPS = structs_WHERE_name_CONTAINS_SUBSTRING.find (
		access.DB (),
		"VItAmIn B"
	)
	structs_LOWER = structs_WHERE_name_CONTAINS_SUBSTRING.find (
		access.DB (),
		"vitamin b"
	)

	for struct in structs:
		print (struct)

	assert (len (structs) >= 6);

	assert (len (structs) == len (structs_VAR_CAPS))
	assert (len (structs) == len (structs_LOWER))

	return;
	
def CHECK_2 ():	
	structs = structs_WHERE_name_CONTAINS_SUBSTRING.find (access.DB (), "Magnesium")
	
	REGIONS = []
	for struct in structs:
		print (struct)
		REGIONS.append (struct ["region"])

	assert (len (structs) >= 1);
	assert (30 in REGIONS);


	return;
	
checks = {
	"Structs have a name that contains 'vitamin b'": CHECK_1,
	"Struct has a name that contains 'Magnesium'": CHECK_2
}