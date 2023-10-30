
'''
	doesn't function yet
'''


PORTION = 100

from fractions import Fraction
import cyte.food.USDA.struct_2.ingredient as quantified_ingredient

def calc (
	usda_food_data, 
	usda_food_data_calculated
):
	energy_nutrient = ""

	assert ("foodNutrients" in usda_food_data)
	food_nutrient = usda_food_data ["foodNutrients"]
	for food_nutrient in food_nutrients:
		assert ("unitName" in food_nutrient ["nutrient"]), food_nutrient;
		unit = food_nutrient ["nutrient"]["unitName"]
	
		if (unit == 'kcal'):
			quantified = quantified_ingredient.calc (
				food_nutrient,
				usda_food_data_calcULATED
			)
			
			print ("quantified", quantified)
		
		

	return;