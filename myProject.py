# Read a list of ingredients from "ingredients.csv"         DONE
# Read user preferences and goals from "preferences.json"   DONE
# Writes a meal plan "meal_plan.txt"                        DONE
# Writes a shopping list "shopping_list.txt"

# Implement an algorithm to recommend recipes based on available ingredients and user preferences.                  NEEDS LOTS OF IMPROVEMENT
# Create a shopping list generator that identifies additional ingredients needed for the selected recipes

import csv
import json
import matplotlib.pyplot as plt

# Global data structures
ingredients = []        # global list of ingredients
preferences = {}        # global dictionary for preferences
recipes = {}            # global dictionary for recipes
meal_plan = {}          # dictionary of recipes in the meal plan

# Global Variables
acceptanceVal = 0
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

# Find the best meal that could be added to meal plan from available from recipes. Return its name.
def find_best():
    best = [0, None]      # i score, name
    for recipe_name, recipe_info in recipes.items():
        nutrition = recipe_info.get('nutrition', {})
        i = getImportance(nutrition)
        if i > best[0]:
            best[0] = i
            best[1] = recipe_name
    if best[1] is not None:     # failsafe in the event that recipes.json has less than 7 available recipes
#        print(f"Highest scoring dish is {best[1]} with a score of {best[0]}!")
        return best[1]
    else:
        print("No unused recipes left.")

def initialize_meal_plan():
    print("Initializing Meal Plan...")
    for i in range (7):
        recipe_name = find_best()
        the_recipe = recipes.pop(recipe_name)
        meal_plan.update({recipe_name: the_recipe})
    print("Meal Plan Has Been Initialized.")

# this function returns the score of the current meal plan. 
# If a recipe name is passed, it returns what the score of the meal plan would be without that recipe
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
    if n > 0:
        score = round(score/n, 4)
    else:
        print("ERROR, n is 0 for some reason!")
    return score

# removes the recipe from meal plan, then adds it back to recipes dictionary
# finds the new best recipe. If it's the same as the removed one, then return false (needs to be added back, is it?)
def replace_recipe(recipe_name):
    removed = {recipe_name: meal_plan.pop(recipe_name)}
    recipes.update(removed)
    new_recipe_name = find_best()
    if new_recipe_name == recipe_name:
        recipes.pop(recipe_name)
        meal_plan.update(removed)
        return False
    else:
        the_recipe = recipes.pop(new_recipe_name)
        meal_plan.update({new_recipe_name: the_recipe})
#        print(f"Replacing {recipe_name} with {new_recipe_name}, giving us a score of {get_meal_score()}")
        return True


def convert_to_units_dict(ingredients_data):
    ingredient_units = {}
    for item in ingredients_data:
        name = item["name"]
        quantity = item["quantity"]
        unit = item["unit"]
        ingredient_units[name] = {"quantity": quantity, "unit": unit}
    return ingredient_units



def generate_shopping_list(meal_plan, ingredient_units):
    shopping_list = {}
    for recipe_name, details in meal_plan.items():
        ingredients = details.get("ingredients", {})
        for ingredient, qty in ingredients.items():
            if ingredient in shopping_list:
                shopping_list[ingredient] += qty
            else:
                shopping_list[ingredient] = qty

    adjusted_shopping_list = {}
    for ingredient, total_qty in shopping_list.items():
        if ingredient in ingredient_units:
            base_qty = ingredient_units[ingredient]["quantity"]
            unit = ingredient_units[ingredient]["unit"]
            adjusted_qty = total_qty / base_qty

            # Calculate adjusted quantity, ensuring it is a whole number
            if adjusted_qty >= 1:
                adjusted_qty = int(round(adjusted_qty))
            else:
                # For values less than 1, we use total_qty in grams/ml
                adjusted_qty = int(total_qty)
                unit = "grams" if "grams" in ingredient_units[ingredient]["unit"] else "ml"

            adjusted_shopping_list[ingredient] = f"{adjusted_qty} {unit}"
        else:
            adjusted_shopping_list[ingredient] = f"{int(total_qty)} grams"

    return adjusted_shopping_list


def save_shopping_list_to_file(shopping_list, filename="shopping_list.txt"):
    with open(filename, "w") as file:
        file.write("Shopping List for the Week\n")
        file.write("==========================\n")
        for item, qty_with_unit in shopping_list.items():
            file.write(f"{item}: {qty_with_unit}\n")
    print(f"Shopping list saved to {filename}")




# Then finds the best recipe in recipes to replace it with
def improve_meal_plan():
    current_score = get_meal_score()
    print(f"Trying to Improve Meal Score of {current_score}...")
    if current_score >= 1 - (acceptanceVal + recursion_count[0]* 0.001):
        print("\nTHE MEAL PLAN SATISFIES PREFERENCES!\n")
        return  # meal plan is ready
    else:
        # find the recipe that has the best impact if removed
        # list of all the meals and the score if they were removed. The highest score is the least important
        meal_scores = []
        for name, item in meal_plan.items():   
            meal_score = get_meal_score(name)
            meal_scores.append((name, meal_score))
        meal_scores.sort(key=lambda x: x[1], reverse=True)

        # try to replace least important first. If it can't be replaced to improve the score, try the next one
        for i in range(0, len(meal_scores)):
            if replace_recipe(meal_scores[i][0]):
                recursion_count[0] += 1
                improve_meal_plan()
                return
            else:
                if (i + 1) < len(meal_scores):
#                    print(f"Replacing {meal_scores[i][0]} can't improve the score. Trying {meal_scores[i + 1][0]}")
                    pass
                else:
                    print("Meal Plan Cannot Be Further Improved")

# Creates meal_plan.txt and writes helpful information into it.
# We need to make sure it displays the information the assignment wants from us
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
        file.write(f"\n\nRecursive Iteration Count: {recursion_count[0]}")

# Plotting function 
def plot_daily_nutrition():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    daily_nutrients = {day: {} for day in days}

    for day, (recipe_name, recipe) in zip(days, meal_plan.items()):
        daily_nutrients[day] = recipe.get('nutrition', {})

    nutrients = list(next(iter(daily_nutrients.values())).keys())
    nutrient_data = {nutrient: [daily_nutrients[day][nutrient] for day in days] for nutrient in nutrients}
    
    fig, ax = plt.subplots()
    bottom = [0] * len(days)
    
    for nutrient in nutrients:
        ax.bar(days, nutrient_data[nutrient], label=nutrient, bottom=bottom)
        bottom = [bottom[i] + nutrient_data[nutrient][i] for i in range(len(days))]
    
    ax.set_xlabel("Day of Week")
    ax.set_ylabel("Amount")
    ax.set_title("Daily Nutrient Breakdown")
    ax.legend()
    
    plt.show()
    
if __name__ == "__main__":
    # read everything
    read_ingredients('ingredients.csv')
    read_preferences('preferences.json')
    read_recipes('recipes.json')

    initialize_meal_plan()
    improve_meal_plan()
    print(f"This algorithm took {recursion_count[0]} iterations to complete!")
    write_meal_plan()
    ingredient_units = convert_to_units_dict(ingredients_data)
    shopping_list = generate_shopping_list(meal_plan, ingredient_units)
    save_shopping_list_to_file(shopping_list)

    # Call the plotting function
    plot_daily_nutrition()


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
