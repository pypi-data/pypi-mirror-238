

'''
	import cyte.structs.DB.PATH as structs_DB_PATH
	PATH = structs_DB_PATH.find ()
'''

'''
	USE CUSTOM PATH:
	
	from cyte.structs.DB.PATH import DB_PATH
'''

'''
def PATH ():
	import pathlib
	from os.path import dirname, join, normpath
	THIS_FOLDER = pathlib.Path (__file__).parent.resolve ()
	return normpath (join (THIS_FOLDER, "structs.json"))
'''


import pathlib
from os.path import dirname, join, normpath

THIS_FOLDER = pathlib.Path (__file__).parent.resolve ()

PATHS = {
	"DB": normpath (join (THIS_FOLDER, "structs.json"))
}

def find ():
	return PATHS ["DB"]




