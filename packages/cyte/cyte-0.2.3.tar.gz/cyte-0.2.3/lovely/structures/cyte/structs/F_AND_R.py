


import glob
import os.path

def START (
	GLOB = "",
	
	find = "",
	REPLACE_WITH = ""
):
	FILES = glob.glob (GLOB, recursive = True)

	for FILE in FILES:
		IS_FILE = os.path.isfile (FILE) 
	
		if (IS_FILE == True):
			print (FILE)

	for FILE in FILES:
		IS_FILE = os.path.isfile (FILE) 
	
		if (IS_FILE == True):			
			try:
				with open (FILE) as FP_1:
					ORIGINAL = FP_1.read ()
					NEW_STRING = ORIGINAL.replace (find, REPLACE_WITH)
			
				if (ORIGINAL != NEW_STRING):
					print ("replacing:", FILE)
					#print ("NEW_STRING:", NEW_STRING)
					
					with open (FILE, "w") as FP_2:
						FP_2.write (NEW_STRING)
			
			except Exception as E:
				print ("EXCEPTION:", E)
				


import pathlib
from os.path import dirname, join, normpath
THIS_FOLDER = pathlib.Path (__file__).parent.resolve ()
	
START (
	GLOB = str (THIS_FOLDER) + "/DB/**/*",
	
	find = '"REGION"',
	REPLACE_WITH = '"region"'
)