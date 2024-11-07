# Read a list of ingredients from "ingredients.csv"         DONE
# Read user preferences and goals from "preferences.json"   DONE
# Writes a meal plan "meal_plan.txt"                        DONE
# Writes a shopping list "shopping_list.txt"

# Implement an algorithm to recommend recipes based on available ingredients and user preferences.                  NEEDS LOTS OF IMPROVEMENT
# Create a shopping list generator that identifies additional ingredients needed for the selected recipes

import csv
import json

# Global data structures
ingredients = []        # global list of ingredients
preferences = {}        # global dictionary for preferences
recipes = {}            # global dictionary for recipes
meal_plan = {}          # dictionary of recipes in the meal plan

# Global Variables
acceptanceVal = 0.05
recursion_count = [0]

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

# this function returns prints information, and returns the score of the current meal plan. Unfinished
def get_meal_score(filter_recipe = None):       # filter_recipe is used after we build our initial meal plan
    score = 0
    total_nutrients = {}        # stores total 
    for name, item in meal_plan.items():
        if name != filter_recipe:
            for nutrient, value in item.get('nutrition').items():
                if nutrient not in total_nutrients.keys():
                    total_nutrients.update({nutrient: value})
                else:
                    total_nutrients[nutrient] += value
    if filter_recipe is not None:
        pass
#        print(f"SCORING WITHOUT {filter_recipe}!!")
    for nutrient, value in total_nutrients.items():
        if nutrient in preferences.keys():
            goal = preferences.get(nutrient)
#            print(f"{nutrient} has a score of {round(1 - abs(goal - value)/goal, 4)}!")
            score += 1 - abs(goal - value)/goal
    n = len(total_nutrients)
    score = round(score/n, 4)
    if filter_recipe is None:
        pass
        print(f"The Current Meal Score is: {score}")
        for nutrient, value in total_nutrients.items():
            pass
#            print(f"Total {nutrient}: {value}")
    else:
        pass
#        print(f"The Current Meal Score without {filter_recipe} is: {score}")
    return score

def replace_recipe(recipe_name):
    removed = {recipe_name: meal_plan.pop(recipe_name)}
    recipes.update(removed)
    find_best()

# Removes the recipe from meal_plan
# Adds it back into recipes
# Then finds the best recipe in recipes to replace it with
def improve_meal_plan():
    current_score = get_meal_score()
    if current_score >= 1 - (acceptanceVal + recursion_count[0]* 0.001):
        print("\nTHE MEAL PLAN SATISFIES PREFERENCES!\n")
        return  # meal plan is ready
    else:
        best_score = [0, ""]                # score, name

        # find the recipe that has the best impact if removed
        for name, item in meal_plan.items():    
            this = get_meal_score(name)
            if this > best_score[0]:
                best_score[0] = this
                best_score[1] = name
        print(f"We are replacing {best_score[1]}, since the meal plan has the highest score of {best_score[0]} without it!")
        replace_recipe(best_score[1])
        recursion_count[0] += 1
        improve_meal_plan()

def write_meal_plan():
    with open('meal_plan.txt', "w") as file:
        file.write("The Meals: ")
        for meal in meal_plan.keys():
            file.write(f"{meal}, ")
        file.write(f"\n\nThe Meal Score: {get_meal_score()}")
        file.write(f"\n\nNutritional Values:")
        total_nutrients = {}        # stores total 
        for name, item in meal_plan.items():
            for nutrient, value in item.get('nutrition').items():
                if nutrient not in total_nutrients.keys():
                    total_nutrients.update({nutrient: value})
                else:
                    total_nutrients[nutrient] += value
        for name, value in total_nutrients.items():
            file.write(f"\n{name}: {value}")
        file.write(f"\n\nRecipe Pool Size: {len(meal_plan) + len(recipes)}\nRecipes Used: {len(meal_plan)}\nRecipes Not Used: {len(recipes)}")

if __name__ == "__main__":
    # read everything
    read_ingredients('ingredients.csv')
    read_preferences('preferences.json')
    read_recipes('recipes.json')

    for i in range (7):
        find_best()
        pass

    improve_meal_plan()
    print(f"This algorithm took {recursion_count[0]} iterations to complete!")
    write_meal_plan()


"""
for name, item in meal_plan.items():
    print(f"{name} has:")
    for nutrient, value in item.get('nutrition').items():
        print(f" {nutrient}: {value}")


# you can use this to see what the meal plan items look like
for key, value in meal_plan.items():
    print(f"Key: {key}")
    print(f"Value: {value}")


for item in meal_plan.values().get('ingredients'):
    print(item)

# this is an example of how to access nutrition items
print(f"CALORIES: {preferences.get('calories')}")
"""
