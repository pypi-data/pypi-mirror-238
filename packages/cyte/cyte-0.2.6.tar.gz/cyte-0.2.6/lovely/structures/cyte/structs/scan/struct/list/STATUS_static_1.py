



'''
	python3 STATUS.py "structs/scan/struct/list/STATUS_static_1.py"
'''

def PATH ():
	import pathlib
	from os.path import dirname, join, normpath
	THIS_FOLDER = pathlib.Path (__file__).parent.resolve ()
	return normpath (join (THIS_FOLDER, "structs.json"))


def CHECK_1 ():
	import cyte.structs.DB.access as access
	import cyte.structs.scan.struct.list as structs_LIST
	LIST = structs_LIST.find (access.DB (PATH ()))

	assert (len (LIST) == 52), len(LIST)
	
	
checks = {
	"static, list": CHECK_1
}