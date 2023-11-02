
import cyte.supplements.NIH.struct_2.ingredient.quantified as quantified_ingredient 


def traverse (
	ingredient_rows = [],
	NIH_supplement_data_struct_2 = {}
):
	print (type (NIH_supplement_data_struct_2))

	ingredients = []
	for ingredient in ingredient_rows:
		quantified = quantified_ingredient.calc (
			ingredient, 
			NIH_supplement_data_struct_2
		)
		
		if ("nestedRows" in ingredient):
			quantified ["quantified grove"] = traverse (
				ingredient_rows = ingredient ["nestedRows"],
				NIH_supplement_data_struct_2 = NIH_supplement_data_struct_2
			)
		else:
			quantified ["quantified grove"] = []
		
		ingredients.append (quantified)		

	ingredients.sort (
		key = lambda ingredient : ingredient ["name"]
	)

	return ingredients;

'''
	ingredientRows
		nestedRows
			nestedRows
			
		nestedRows
			nestedRows
			nestedRows
				nestedRows
'''
def calc (
	NIH_supplement_data,
	NIH_supplement_data_struct_2
):
	assert ("ingredientRows" in NIH_supplement_data)
	
	ingredient_rows = NIH_supplement_data ["ingredientRows"]
	ingredients = traverse (
		ingredient_rows,
		NIH_supplement_data_struct_2
	)

	return ingredients