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
recipes = {}            # global dictionary for recipes
meal_plan = {}          # dictionary of recipes in the meal plan

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

def read_recipes(file_path):
    global recipes
    with open(file_path, mode='r') as file:
        recipes = json.load(file)
    if(preferences.get('diet') == "vegetarian"):
        print("Filtering out non-vegetarian dishes...")
        for recipe in list(recipes.keys()):                    # going through a list of keys
            if recipes[recipe].get('diet') != "vegetarian":
                recipes.pop(recipe)

def print_ingredients():
    print("\nINGREDIENTS:")
    for ingredient in ingredients:
        print(ingredient)
    print("\n")

def print_recipes():
    print("\nRECIPES:")
    for recipe in recipes:
        print(recipe, ":", recipes.get(recipe))
    print("\n")

read_ingredients('ingredients.csv')
read_preferences('preferences.json')
read_recipes('recipes.json')

"""
print_ingredients()
print_recipes()
print("pref:", preferences)
"""

"""
# this function creates meal_plan.txt
def create_meal_plan(recipes, preferences):
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
"""

# this function takes recipe info and returns the i value!
def getImportance(nutrition):
    i = 0
    n = 0
    for nutrient, value in nutrition.items():       # for each nutrient
        if nutrient in preferences.keys():
            goal = preferences.get(nutrient)
            progress = value
            for item in meal_plan.values():
                progress += item.get('nutrition').get(nutrient)
            n += 1
            i += (1 - abs(progress - goal)/goal)
    i = round(i/n, 4)
    return i

# this function prints the importance score of all recipes available
def recipes_information():
    for recipe_name, recipe_info in recipes.items():
        print(f"{recipe_name}.")
        nutrition = recipe_info.get('nutrition', {})
        for nutrient, value in nutrition.items():
            print(f"   {nutrient}: {value}.")
        print(f"   {recipe_name}'s importance score: {getImportance(nutrition)}")
    for nutrition, value in preferences.items():
        print(f"{nutrition} wanted: {value}")

# this is an example of how to access nutrition items
# print(f"CALORIES: {preferences.get('calories')}")



# Find the best dish available from recipes, adds it to the meal_plan list, and removes the recipe from the recipe list
def find_best():
    best = [0, None]      # i score, name
    for recipe_name, recipe_info in recipes.items():
        nutrition = recipe_info.get('nutrition', {})
        i = getImportance(nutrition)
        if i > best[0]:
            best[0] = i
            best[1] = recipe_name
    if best[1] is not None:     # failsafe in the event that recipes.json has less than 7 available recipes
        print(f"Highest scoring dish is {best[1]} with a score of {best[0]}!")
        the_recipe = recipes.pop(best[1])
        meal_plan.update({best[1]: the_recipe})

for i in range (7):
    find_best()
    pass

# this function returns the score of the current meal plan. Unfinished
def meal_score():
    score = 0
    n = len(meal_plan)
    total_nutrients = {}        # stores total 
    for name, item in meal_plan.items():
        for nutrient, value in item.get('nutrition').items():
            if nutrient not in total_nutrients.keys():
                total_nutrients.update({nutrient: value})
            else:
                total_nutrients[nutrient] += value

    for nutrient, value in total_nutrients.items():
        if nutrient in preferences.keys():
            goal = preferences.get(nutrient)
            score += 1 - abs(goal - value)/goal
    score = round(i/n, 4)

    print(f"Current Meal Score: {score}")
    for nutrient, value in total_nutrients.items():
        print(f"Total {nutrient}: {value}")
    return score

meal_score()

"""
for name, item in meal_plan.items():
    print(f"{name} has:")
    for nutrient, value in item.get('nutrition').items():
        print(f" {nutrient}: {value}")


# you can use this to see what the meal plan items look like
for item in meal_plan.items():
    print(item)
"""
