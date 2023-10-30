



'''
	python3 status.py "_interpret/STATUS_unit_kind.py"
'''

import cyte._interpret.unit_kind as UNIT_kind

from fractions import Fraction

def CHECK_1 ():
	assert (UNIT_kind.calc ("ml") == "volume")
	assert (UNIT_kind.calc ("fl oz") == "volume")
	
	assert (UNIT_kind.calc ("GRAM") == "mass")
	assert (UNIT_kind.calc ("gram") == "mass")
	
	assert (UNIT_kind.calc ("IU") == "effectual mass")

	assert (UNIT_kind.calc ("kcal") == "energy")


checks = {
	"CHECK 1": CHECK_1
}
	


