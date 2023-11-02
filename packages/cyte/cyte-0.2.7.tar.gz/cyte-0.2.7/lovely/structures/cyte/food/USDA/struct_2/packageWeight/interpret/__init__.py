



UNIT_LEGEND = {	
	"oz": "OUNCES",
	"lb": "POUNDS",
	"lbs": "POUNDS",

	"kg": "KILOGRAMS",
	"g": "GRAMS",
	"mg": "MICROGRAMS",
	"mcg": "MILLIGRAMS",
	
	"fl oz": "FLUID OUNCES",
	"quart": "QUART",
	
	"ml": "MILLILITERS",
	"l": "LITERS"
}

VOLUME_UNITS = [ 
	"fl oz", 
	"quart",
	
	"ml",
	"l"
]

mass_UNITS = [ 
	"oz", 
	"lb", 
	"lbs",
	
	"g", 
	"kg", 
	"mg", 
	"mcg" 
]


'''
	lb -> g

	oz -> g
	
	g -> g
'''

from fractions import Fraction
import cyte.mass.swap as mass_swap
import cyte.volume.swap as VOLUME_swap

import json

def SPLIT_LABEL (LABEL):
	ONE = ""
	TWO = ""

	PART_2 = False
	
	SELECTOR = 0
	LAST_INDEX = len (LABEL) - 1
	while (SELECTOR <= LAST_INDEX):
		CHARACTER = LABEL [SELECTOR]
		
		#print ("CHARACTER:", CHARACTER)
	
		if (CHARACTER == " "):
			SELECTOR += 1
			break;
		else:	
			ONE += CHARACTER
			
			
		SELECTOR += 1
	
		
	while (SELECTOR <= LAST_INDEX):
		CHARACTER = LABEL [SELECTOR]
		TWO += CHARACTER
		SELECTOR += 1
	
	return [ ONE.lower (), TWO.lower () ]


def INTERPRET (PARAM):
	if (type (PARAM) != str):
		return [ "?", "POUNDS" ]
		
	RETURNS = {}
		
	SPLITS = PARAM.split ("/")
	
	print ("SPLITS:", SPLITS)
	
	VOLUME_IS_KNOWN = False
	mass_IS_KNOWN = False
	
	for SPLIT in SPLITS:
		[ AMOUNT, UNIT ] = SPLIT_LABEL (SPLIT)
		#[ AMOUNT, UNIT ] = SPLIT.split (" ")
		
		print (AMOUNT, UNIT)
		
		print (
			json.dumps (
				{
					"AMOUNT": AMOUNT, 
					"UNIT": UNIT 
				}, 
				indent = 4
			)
		)
		
		assert (UNIT in UNIT_LEGEND), f"unit: '{ UNIT }'"
		
		if (UNIT in VOLUME_UNITS):
			VOLUME_IS_KNOWN = True
		elif (UNIT in mass_UNITS):
			mass_IS_KNOWN = True;
		else:
			print ("unit:", UNIT)
			raise Exception ("Unit was not found in volume of mass units.")
		
		
		SPRUCED_UNIT = UNIT_LEGEND [ UNIT ]
		
		RETURNS [ SPRUCED_UNIT ] = AMOUNT
	
	
	print ("VOLUME_IS_KNOWN:", VOLUME_IS_KNOWN)
	print ("mass_IS_KNOWN:", mass_IS_KNOWN)
	print ("RETURNS", RETURNS)

	if (mass_IS_KNOWN):
	
		
		#
		#	IF GRAMS IS NOT IN RETURNS,
		# 	THEN TRY TO find ANOTHER UNIT THAT
		#	CAN BE swapPED INTO GRAMS.
		#
		if ("GRAMS" not in RETURNS):
			if ("OUNCES" in RETURNS):
				AMOUNT_OF_OUNCES = RETURNS ["OUNCES"]
			
				RETURNS ["GRAMS"] = str (float (
					mass_swap.START (
						[ AMOUNT, "OUNCES" ],
						"GRAMS"
					)
				))
				
			elif ("POUNDS" in RETURNS): 
				AMOUNT = RETURNS ["GRAMS"]
			
				RETURNS ["GRAMS"] = str (float (
					mass_swap.START (
						[ AMOUNT, "POUNDS" ],
						"GRAMS"
					)
				))
				
			else:
				raise Exception ("COULD NOT DETERMINE PACKAGE mass IN GRAMS.")

		assert ("GRAMS" in RETURNS)

		
		print ("RETURNS:", RETURNS)
		
		#
		#	IF POUNDS IS NOT IN RETURNS,
		# 	THEN TRY TO find ANOTHER UNIT THAT
		#	CAN BE swapPED INTO POUNDS.
		#
		if ("POUNDS" not in RETURNS):
			if ("OUNCES" in RETURNS):
				AMOUNT = RETURNS ["OUNCES"]
			
				RETURNS ["POUNDS"] = str (float (
					mass_swap.START (
						[ AMOUNT, "OUNCES" ],
						"POUNDS"
					)
				))
				
			elif ("GRAMS" in RETURNS): 
				AMOUNT = RETURNS ["GRAMS"]
			
				RETURNS ["POUNDS"] = str (float (
					mass_swap.START (
						[ AMOUNT, "GRAMS" ],
						"POUNDS"
					)
				))
				
			else:
				raise Exception ("'pounds' per package could not be calculated.")

		assert ("POUNDS" in RETURNS)
		
	if (VOLUME_IS_KNOWN):
		#
		#	plan:
		#		calculate ([ "liters", "fluid ounces" ])
		#
	
		def calculate ():
			return;
		
	
		if ("LITERS" not in RETURNS):
			if ("FLUID OUNCES" in RETURNS):
				UNIT_1 = "FLUID OUNCES"
				UNIT_2 = "LITERS"

				AMOUNT = RETURNS [ UNIT_1 ]
				RETURNS [ UNIT_2 ] = str (float (
					VOLUME_swap.START (
						[ AMOUNT, UNIT_1 ],
						UNIT_2
					)
				))
				
			elif ("MILLILITERS" in RETURNS): 
				UNIT_1 = "MILLILITERS"
				UNIT_2 = "LITERS"

				AMOUNT = RETURNS [ UNIT_1 ]
				RETURNS [ UNIT_2 ] = str (float (
					VOLUME_swap.START (
						[ AMOUNT, UNIT_1 ],
						UNIT_2
					)
				))
				
			else:
				raise Exception ("'liters' per package could not be calculated.")

	return RETURNS

