


'''
	python3 STATUS.py "volume/swap/STATUS_1.py"
'''

import cyte.volume.swap as VOLUME_swap

from fractions import Fraction

def CHECK_EQ (ONE, TWO, FLOAT = False):
	if (ONE != TWO):
		if (FLOAT == True):
			raise Exception (
				f'{ float (ONE) } != { float (TWO) }'
			)
		
		else:
			raise Exception (
				f'{ ONE } != { TWO }'
			)
		
	return;


def CHECK_1 ():
	#		1 fl oz = 29.5735 millilitres 
	#		1 fl oz = 0.0295735 liters
	#
	#		1 liter = 1 / 0.0295735 fl oz
	CHECK_EQ (
		VOLUME_swap.START ([ 1, "FL OZ" ], "milliliters"),
		Fraction (29.5735)
	)
	CHECK_EQ (
		VOLUME_swap.START ([ 1, "FL OZ" ], "liters"),
		Fraction (29.5735) * Fraction (1, 1000),
		FLOAT = True
	)
	CHECK_EQ (
		VOLUME_swap.START ([ 1, "liters" ], "fluid ounces"),
		Fraction (1, (Fraction (29.5735) * Fraction (1, 1000))),
		FLOAT = True
	)
	
	

def CHECK_2 ():
	CHECK_EQ (
		VOLUME_swap.START ([ 1, "fluid OUNCES" ], "mL"),
		Fraction (29.5735)
	)
	CHECK_EQ (
		VOLUME_swap.START ([ 1, "FL OZ" ], "liters"),
		Fraction (29.5735) * Fraction (1, 1000),
		FLOAT = True
	)

	CHECK_EQ (
		VOLUME_swap.START ([ 1, "litres" ], "fluid ounces"),
		Fraction (1, (Fraction (29.5735) * Fraction (1, 1000))),
		FLOAT = True
	)

	return;
	
def CHECK_3 ():
	'''
	EXCEPTION_CALLED = False
	try:
		CHECK_EQ (
			VOLUME_swap.START ([ 1, "fluid OUNCES" ], "ml"),
			Fraction (29.5735)
		)
		
	except Exception as E:
		assert (str (E) == "Unit 'ml' was not found.")
		EXCEPTION_CALLED = True

	assert (EXCEPTION_CALLED == True)
	'''

	
checks = {
	"fraction checks": CHECK_1,
	"fraction checks, alternate spellings": CHECK_2,
	
	"exceptions": CHECK_3
}