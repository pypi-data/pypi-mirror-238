

'''


'''
import cyte.food.USDA.struct_2.ingredient as quantified_ingredient

def calc (
	usda_food_data, 
	usda_food_data_calculated
):
	ingredients = []

	assert ("foodNutrients" in usda_food_data)
	food_nutrients = usda_food_data ["foodNutrients"]
	
	for food_nutrient in food_nutrients:
		quantified = quantified_ingredient.calc (
			food_nutrient,
			usda_food_data_calculated
		)
		
		if (quantified != "energy"):
			ingredients.append (quantified)
	

	return ingredients