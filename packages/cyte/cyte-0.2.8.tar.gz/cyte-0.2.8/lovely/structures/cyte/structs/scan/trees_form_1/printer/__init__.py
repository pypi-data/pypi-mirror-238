

'''
import cyte.structs.scan.trees_form_1.printer as trees_form_1_printer
trees_form_1_printer.write (structs)
'''
def write (structs, level = 0):
	indent = " " * (level * 4)
	structs.sort (key = lambda struct : struct ["names"][0])

	for struct in structs:
		print (f"{ indent }{ struct['names'] } { struct['region'] }")

		if ("includes structs" in struct):
			write (struct ["includes structs"], level = (level + 1))

	return;
	
