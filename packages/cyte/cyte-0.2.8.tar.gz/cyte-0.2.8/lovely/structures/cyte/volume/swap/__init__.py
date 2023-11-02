
'''
	utilizes:
		US Customary
		System International
'''


'''
	import cyte.volume.swap as volume_swap
	volume_swap.START ([ 1, "FL OZ" ], "LITER")
'''

from fractions import Fraction 


GRAMS_TO_POUNDS = Fraction (1, Fraction (453.59237))
POUNDS_TO_OUNCES = 16

#
#	https://en.wikipedia.org/wiki/Fluid_ounce
#		1 fl oz = 29.5735 millilitres 
#		1 fl oz = 0.0295735 liters
#
#		1 liter = 1 / 0.0295735 fl oz
#

#
#	Fraction (1, (Fraction (29.5735) * Fraction (1, 1000)))
#
FLUID_OUNCES_TO_LITERS = Fraction (29.5735) * Fraction (1, 1000)


CONVERSIONS = {
	#
	#	1 liter = 33.8140227 US ounce 
	#
	"liters": {
		"fluid ounces": Fraction (1, FLUID_OUNCES_TO_LITERS),
		"milliliters": Fraction (1000, 1)
	},
	
	#
	#	1 mL = 1/1000 L 
	#
	"milliliters": {
		"fluid ounces": Fraction (1, FLUID_OUNCES_TO_LITERS) * Fraction (1, 1000),
		"liters": Fraction (1, 1000)
	},
	
	#
	#	1 fl oz = 1/32 quarts 
	#
	"fluid ounces": {
		"quarts": Fraction (1, 32),
		
		"milliliters": FLUID_OUNCES_TO_LITERS * Fraction (1000, 1),
		"liters": FLUID_OUNCES_TO_LITERS
	},
	
	"quarts": {
		"fluid ounces": 32
	}
}


CASE_INSENSITIVE_GROUPS = [
	[ "liters", "litres", "liter", "l" ],
	[ "milliliters", "millilitres", "millilitre", "ml" ],

	[ "fluid ounces", "fluid ounce", "fl oz" ]
]

#
#	
#
CASE_SENSITIVE_GROUPS = []

'''
CASE_SENSITIVE_GROUPS = [
	[ "liters", "L" ],
	[ "milliliters", "mL" ],
]
'''

def find_UNIT (TO_find):
	LOWER_CASE_UNIT = TO_find.lower ()
	for CASE_INSENSITIVE_GROUP in CASE_INSENSITIVE_GROUPS:		
		for UNIT in CASE_INSENSITIVE_GROUP:
			if (UNIT == LOWER_CASE_UNIT):
				return CASE_INSENSITIVE_GROUP [0]
				
	for CASE_SENSITIVE_GROUP in CASE_SENSITIVE_GROUPS:		
		for UNIT in CASE_SENSITIVE_GROUP:
			if (UNIT == TO_find):
				return CASE_SENSITIVE_GROUP [0]
	
	raise Exception (f"Unit '{ TO_find }' was not found.")



def START (FROM, TO_UNIT):
	[ FROM_AMOUNT, FROM_UNIT ] = FROM;

	FROM_UNIT = find_UNIT (FROM_UNIT)
	TO_UNIT = find_UNIT (TO_UNIT)

	print ("FROM_UNIT:", FROM_UNIT)
	assert FROM_UNIT in CONVERSIONS, f'"{ FROM_UNIT }" was not found"'
	
	print ("TO_UNIT:", TO_UNIT)
	assert (TO_UNIT in CONVERSIONS [ FROM_UNIT ]), f'"{ TO_UNIT }" was not found in conversions."'

	return CONVERSIONS [ FROM_UNIT ] [ TO_UNIT ] * Fraction (FROM_AMOUNT);