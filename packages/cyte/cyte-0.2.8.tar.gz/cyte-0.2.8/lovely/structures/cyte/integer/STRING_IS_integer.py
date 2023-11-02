
'''
import cyte.integer.STRING_IS_integer as STRING_IS_integer
STRING_IS_integer.CHECK ("1234")
'''

def CHECK (STRING):
	if (len (STRING) == 0):
		return False;
		
	integer_CHARACTERS = [ 
		"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
	]
	for CHARACTER in STRING:
		if (CHARACTER not in integer_CHARACTERS):
			return False;

	return True