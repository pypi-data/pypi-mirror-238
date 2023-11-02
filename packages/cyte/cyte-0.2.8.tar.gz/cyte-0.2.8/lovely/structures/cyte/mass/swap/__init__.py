

'''
	https://www.wolframalpha.com/input?i=gram+to+pound
'''

'''
	GOAL:
		mass ([ 432, "GRAMS" ], "POUNDS")
'''

'''
	import cyte.mass.swap as mass_swap
	mass_swap.START ([ 432, "GRAMS" ], "POUNDS")
'''

from fractions import Fraction 

GRAMS_TO_POUNDS = Fraction (1, Fraction (453.59237))
POUNDS_TO_OUNCES = 16

CONVERSIONS = {
	"grams": {
		"pounds": GRAMS_TO_POUNDS,
		"ounces": Fraction (GRAMS_TO_POUNDS, POUNDS_TO_OUNCES),
		
		"milligrams": Fraction (1000, 1),
		"micrograms": Fraction (1000000, 1)
	},
	"milligrams": {		
		"micrograms": Fraction (1000, 1),
		"grams": Fraction (1, 1000)
	},
	"micrograms": {
		"grams": Fraction (1, 1000000),
		"milligrams": Fraction (1, 1000)
	},
	
	
	#
	#	avroidupois
	#
	"pounds": {
		"ounces": 16,
		"grams": Fraction (453.59237)
	},
	"ounces": {
		"pounds": Fraction (1, 16),
		"grams": Fraction (28.349523125)
	},
	
	#
	#	troy
	#
	"troy pounds": {},
	"troy ounces": {}	
}

#
#	these need to be lowercase currenly
#
GROUPS = [
	[ "grams", "gram(s)", "gram", "g", "grm" ],
	[ "milligrams", "milligram", "mg" ],
	[ "micrograms", "microgram", "mcg" ],

	[ "pounds", "pound", "lbs", "lb" ],
	[ "ounces", "ounce", "oz", "ozs" ],
]


def find_UNIT (TO_find):
	for GROUP in GROUPS:		
		for UNIT in GROUP:
			if (UNIT == TO_find):
				return GROUP [0]
	
	#print ("unit to find:", TO_find)
	raise Exception ("Unit was not found.")



def START (FROM, TO_UNIT):
	[ FROM_AMOUNT, FROM_UNIT ] = FROM;

	FROM_UNIT = find_UNIT (FROM_UNIT.lower ())
	TO_UNIT = find_UNIT (TO_UNIT.lower ())

	if (FROM_UNIT == TO_UNIT):
		return FROM_AMOUNT

	assert (FROM_UNIT in CONVERSIONS), { "FROM_UNIT": FROM_UNIT, "TO_UNIT": TO_UNIT }
	assert (TO_UNIT in CONVERSIONS [ FROM_UNIT ]), { "FROM_UNIT": FROM_UNIT, "TO_UNIT": TO_UNIT }

	return CONVERSIONS [ FROM_UNIT ] [ TO_UNIT ] * Fraction (FROM_AMOUNT);