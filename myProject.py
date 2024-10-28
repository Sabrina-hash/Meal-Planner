# Read a list of ingredients from "ingredients.csv"
# Read user preferences and goals from "preferences.json"
# Writes a meal plan "meal_plan.txt"
# Writes a shopping list "shopping_list.txt"

# Get recipies from somewhere?

# Implement an algorithm to recommend recipes based on available ingredients and user preferences.
# Develop a meal planning algorithm that creates a weekly meal plan, ensuring nutritional balance and variety.
# Create a shopping list generator that identifies additional ingredients needed for the selected recipes

import csv

# Global list to store ingredients
ingredients = []

def read_ingredients(file_path):
    global ingredients
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            ingredients.append({
                'name': row['name'],
                'quantity': int(row['quantity']),
                'unit': row['unit']
            })

read_ingredients('ingredients.csv')
print(ingredients)
