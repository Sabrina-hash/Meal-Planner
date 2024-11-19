# python -m unittest test_myProject.py

import unittest
import myProject

class TestMealPlanner(unittest.TestCase):

    def setUp(self):
        self.preferences = {'calories': 200, 'protein': 50}
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

if __name__ == '__main__':
    unittest.main()
