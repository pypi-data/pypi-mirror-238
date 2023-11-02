
'''
	python3 status.py "mass/swap/STATUS_1.py"
'''

import cyte.mass.swap as mass_swap

from fractions import Fraction

def CHECK_1 ():
	assert (float (mass_swap.START ([ 453.59237, "GRAMS" ], "POUNDS")) == 1.0)
	assert (float (mass_swap.START ([ 453.59237, "grams" ], "pounds")) == 1.0)	
	assert (float (mass_swap.START ([ 453.59237, "Gram(s)" ], "pounds")) == 1.0)	
	
	assert (float (mass_swap.START ([ 10, "OUNCES" ], "POUNDS")) == 0.625)
	assert (float (mass_swap.START ([ 10, "OUNCES" ], "GRAMS")) == 283.49523125)	




	
def CHECK_2 ():
	assert (
		mass_swap.START ([ 10, "mcg" ], "g") == 
		Fraction (1, 100000)
	)	
	assert (
		mass_swap.START ([ 10, "mcg" ], "mg") == 
		Fraction (1, 100)
	)	
	
	assert (
		mass_swap.START ([ 10, "mg" ], "g") == 
		Fraction (1, 100)
	)
	
	assert (
		mass_swap.START ([ 10, "g" ], "mg") == 
		Fraction (10000, 1)
	)
	assert (
		mass_swap.START ([ 10, "g" ], "mcg") == 
		Fraction (10000000, 1)
	)
	
checks = {
	"CHECK 1": CHECK_1,
	"CHECK 2": CHECK_2
}