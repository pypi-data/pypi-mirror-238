
'''
import cyte.hygiene._doc.string.valid_characters as validate_characters
validate_characters (string)
'''

valid_characters = "abcdefghijklmnopqrstuvwxyz0123456789"

def start (string):
	for character in string:
		if (character not in valid_characters):
			return False

	return True