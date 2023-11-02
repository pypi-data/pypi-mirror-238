

'''
	attach a product struct to the struct tree
'''

'''
import cyte.structs.scan.trees_form_1.attach as attach_product_struct
attach_product_struct.start (product_struct trees_form_1_grove)
'''
'''
{
	"found": "yes",
	"names": []
}
'''

import cyte.structs.scan.trees_form_1.find.region as find_region


def start (
	product_struct,
	grove
):	
	struct = find_region.start (product_struct["region"], grove)
	struct ["found"] = "yes"
	struct ["ingredient"] = product_struct ["ingredient"]

	return