



'''
	python3 status.py "_interpret/STATUS_unit_kind.py"
'''

import cyte._interpret.unit_kind as UNIT_kind

from fractions import Fraction

def CHECK_1 ():
	assert (UNIT_kind.CALC ("ml") == "volume")
	assert (UNIT_kind.CALC ("fl oz") == "volume")
	
	assert (UNIT_kind.CALC ("GRAM") == "mass")
	assert (UNIT_kind.CALC ("gram") == "mass")
	
	assert (UNIT_kind.CALC ("IU") == "effectual mass")

	assert (UNIT_kind.CALC ("kcal") == "energy")


checks = {
	"CHECK 1": CHECK_1
}
	


