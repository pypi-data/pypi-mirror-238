


'''
import cyte.structs.scan.trees_form_1.for_each as for_each

def for_each_fn (params):
	struct = params.struct;
	level = params.level;

	return;


for_each.start (
	trees_form_1_grove,
	for_each = for_each_fn
)
'''


def start (structs, for_each, level = 0):
	#indent = " " * (level * 4)
	#structs.sort (key = lambda struct : struct ["names"][0])

	for struct in structs:
		#print (f"{ indent }{ struct['names'] } { struct['region'] }")
		
		class params:
			def __init__ (this, struct, level):
				this.struct = struct
				this.level = level
		
		for_each (params (struct, level))

		if ("includes structs" in struct):
			start (struct ["includes structs"], for_each, level = (level + 1))

	return;