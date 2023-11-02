
'''
	caution: not case sensitive
'''

'''
	import cyte._interpret.unit_kind as UNIT_kind
	kind = UNIT_kind.calc ("ml")
'''

VOLUME_UNIT_GROUPS = [
	[ "liters", "litres", "l" ],
	[ "milliliters", "millilitres", "ml" ],

	[ "fluid ounces", "fl oz" ]
]

#
#	maybe these are case sensitive?
#
mass_UNIT_GROUPS = [
	[ "grams", "gram", "g", "grm" ],
	[ "milligrams", "milligram", "mg" ],
	[ "micrograms", "microgram", "mcg" ],

	[ "pounds", "pound", "lbs", "lb" ],
	[ "ounces", "ounce", "oz", "ozs" ],
]

EFFECTUAL_mass_UNIT_GROUPS = [
	[ "IU" ],
	[ "DFE" ],
	[ "NE" ],
	[ "RAE" ],
	[ "mg alpha-tocopherol" ]
]

energy_unit_groups = [
	[ "kcal" ]
]

def calc (UNIT):
	for GROUP in VOLUME_UNIT_GROUPS:
		for GROUP_UNIT in GROUP:
			if (UNIT.lower () == GROUP_UNIT):
				return "volume"

	for GROUP in mass_UNIT_GROUPS:
		for GROUP_UNIT in GROUP:
			if (UNIT.lower () == GROUP_UNIT):
				return "mass"
				
	for GROUP in EFFECTUAL_mass_UNIT_GROUPS:
		for GROUP_UNIT in GROUP:
			if (UNIT.lower () == GROUP_UNIT.lower ()):
				return "effectual mass"
	
	for group in energy_unit_groups:
		for group_unit in group:
			if (UNIT.lower () == group_unit.lower ()):
				return "energy"
	
	return "?"