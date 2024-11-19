# python -m unittest test_myProject.py

import unittest
import myProject

class TestMealPlanner(unittest.TestCase):

    def setUp(self):
        # Mock global variables
#        global preferences, meal_plan
        self.preferences = {'calories': 200, 'protein': 50, 'diet': 'non-vegetarian'}
        self.meal_plan = {}  # Start with an empty meal plan
        self.recipes = {
            'Pasta': {
                'diet': 'vegetarian',
                'ingredients': {'pasta': 100, 'tomato': 50},
                'nutrition': {'calories': 80, 'protein': 20}
            },
            'Chicken Salad': {
                'diet': 'non-vegetarian',
                'ingredients': {'chicken': 150, 'lettuce': 50},
                'nutrition': {'calories': 120, 'protein': 30}
            }
        }

    def test_getImportance(self):
        pasta_importance = myProject.getImportance(self.recipes['Pasta']['nutrition'], self.preferences, self.meal_plan)
        chicken_salad_importance = myProject.getImportance(self.recipes['Chicken Salad']['nutrition'], self.preferences, self.meal_plan)
        self.assertEqual(pasta_importance, 0.4)
        self.assertEqual(chicken_salad_importance, 0.6)

        self.meal_plan.update({'Pasta': self.recipes.get('Pasta')})
        total_importance = myProject.getImportance(self.recipes['Chicken Salad']['nutrition'], self.preferences, self.meal_plan)

        self.assertEqual(total_importance, 1)

    def test_find_best(self):
        best_recipe = myProject.find_best(self.recipes, self.preferences, self.meal_plan)
        self.assertEqual(best_recipe, 'Chicken Salad')

    def test_get_meal_score(self):
        meal_score = myProject.get_meal_score(self.preferences, self.meal_plan)
        self.assertEqual(meal_score, 0)

        self.meal_plan.update({'Chicken Salad': self.recipes.get('Chicken Salad')})
        meal_score = myProject.get_meal_score(self.preferences, self.meal_plan)
        self.assertEqual(meal_score, 0.6)

        self.meal_plan.update({'Pasta': self.recipes.get('Pasta')})
        meal_score = myProject.get_meal_score(self.preferences, self.meal_plan)
        self.assertEqual(meal_score, 1)
        
    def test_replace_recipe(self):
        self.meal_plan.update({'Pasta': self.recipes.get('Pasta')})
        
        self.assertEqual(myProject.replace_recipe('Pasta', self.recipes, self.preferences, self.meal_plan), True)
        self.assertEqual(myProject.replace_recipe('Chicken Salad', self.recipes, self.preferences, self.meal_plan), False)

if __name__ == '__main__':
    unittest.main()
