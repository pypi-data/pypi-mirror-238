

'''
import cyte.recipes.struct_2.ingredients.quantified_grove.write.ingredients_in_grove_count as ingredients_in_grove_count
ingredients_in_grove_count.start ()
'''
def start (
	quantified_grove = [],
	count = 0
):
	for ingredient in quantified_grove:
		count += 1
		print (count, ingredient ["name"])
		
		if ("quantified grove" in ingredient):
			count += start (
				quantified_grove = ingredient ["quantified grove"],
				count = 0
			)

	return count