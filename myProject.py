# Read a list of ingredients from "ingredients.csv"         DONE
# Read user preferences and goals from "preferences.json"   DONE
# Writes a meal plan "meal_plan.txt"
# Writes a shopping list "shopping_list.txt"

# Implement an algorithm to recommend recipes based on available ingredients and user preferences.
# Develop a meal planning algorithm that creates a weekly meal plan, ensuring nutritional balance and variety.
# Create a shopping list generator that identifies additional ingredients needed for the selected recipes

import csv
import json

# Global data structures
ingredients = []        # global list of ingredients
preferences = {}        # global dictionary for preferences
recipies = {}           # global dictionary for recipies

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

def read_preferences(file_path):
    global preferences
    with open(file_path, mode='r') as file:
        data = json.load(file)  # Load the entire JSON data
        all = data.get('user_preferences', {})  # Store only the content of 'user_preferences'
        preferences = all.get('nutritional_goals', {})  # get nutritional goals
        preferences.update({'diet': all.get('diet')})   # add the diet

def read_recipies(file_path):
    global recipies
    with open(file_path, mode='r') as file:
        recipies = json.load(file)

def print_ingredients():
    print("\nINGREDIENTS:")
    for ingredient in ingredients:
        print(ingredient)
    print("\n")

def print_recipies():
    print("\nRECIPIES:")
    for recipie in recipies:
        print(recipie, ":", recipies.get(recipie))
    print("\n")

read_ingredients('ingredients.csv')
read_preferences('preferences.json')
read_recipies('recipies.json')
print_ingredients()
print_recipies()

print("pref:", preferences)


# this function creates meal_plan.txt
def create_meal_plan(recipies, preferences):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    # return meal_plan

# this function creates shopping_list.txt
def generate_shopping_list(recipes, ingredients):
    pass
    # return shopping_list

# we might want something like this
def analyze_nutrition(meal_plan, recipes, preferences, recipe_nutrition):
    pass
    # return nutrition_summary
