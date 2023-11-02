




'''
python3 STATUS.py "integer/STATUS_STRING_IS_integer.py"
'''

import cyte.integer.STRING_IS_integer as STRING_IS_integer

def CHECK_1 ():
	assert (STRING_IS_integer.CHECK ("1234") == True)
	assert (STRING_IS_integer.CHECK ("0") == True)
	assert (STRING_IS_integer.CHECK ("1234781902394871293750182374") == True)
	
	assert (STRING_IS_integer.CHECK ("") == False)
	assert (STRING_IS_integer.CHECK ("1234.43") == False)
	assert (STRING_IS_integer.CHECK ("Z") == False)

	

	return;
	
	
checks = {
	"CHECK 1": CHECK_1
}