import csv
import json
import matplotlib.pyplot as plt

# Global data structures
ingredients = []        # global list of ingredients            [{'name': 'chicken', 'quantity': 500, 'unit': grams}, {}...]
preferences = {}        # global dictionary for preferences     {'calories': 2650, 'protein': 118, 'carbs': 360, 'fat': 85, 'diet': 'vegetarian'}
recipes = {}            # global dictionary for recipes         {'Pasta': {'diet': 'vegetarian', 'ingredients': {'pasta': 100, 'tomato': 50}, 'nutrition': {'calories': 300, ...}}...}
meal_plan = {}          # dictionary of recipes in the meal plan (the same format as recipes)
shopping_list = {}      # dictionary of dictionaries {chicken: {quantity: 10, unit: grams}, rice: {quantity: 20, unit: grams}...etc}

# Keeping track of recursion count
recursion_count = [0]

# myProject.py makes use of global variables for most things, but these data structures are now passed as arguments to accomodate for unit testing

def read_ingredients(file_path):
    global ingredients
    try:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            ingredients = []  # Initialize or clear the global list
            for row in reader:
                ingredients.append({        # each entry of the list is a dictionary with three keys: {name, quanitity, unit}
                    'name': row['name'],
                    'quantity': int(row['quantity']),
                    'unit': row['unit']
                })
        return True
    except Exception as e:
        print(f"Error reading ingredients: {e}")
        return False

def read_preferences(file_path):
    global preferences
    try:
        with open(file_path, mode='r') as file:
            data = json.load(file)  # Load the entire JSON data
            all_prefs = data.get('user_preferences', {})  # Store only the content of 'user_preferences'
            preferences = all_prefs.get('nutritional_goals', {})  # Get nutritional goals
            preferences.update({'diet': all_prefs.get('diet')})  # Add the diet
        return True
    except Exception as e:
        print(f"Error reading preferences: {e}")
        return False

def read_recipes(file_path):
    global recipes
    try:
        with open(file_path, mode='r') as file:
            recipes = json.load(file)
        if preferences.get('diet') == "vegetarian":
            print("Filtering out non-vegetarian dishes...")
            for recipe in list(recipes.keys()):  # Go through a list of keys
                if recipes[recipe].get('diet') != "vegetarian":
                    recipes.pop(recipe)
        return True
    except Exception as e:
        print(f"Error reading recipes: {e}")
        return False

# this function takes recipe info and returns the i value!
# nutrition is in form of:                                  {'calories': 300, 'protein': 25,...}
def getImportance(nutrition, preferences, meal_plan):
    i = 0
    n = 0
    for nutrient in preferences.keys():
        if nutrient != 'diet':
            goal = preferences.get(nutrient)
            progress = nutrition.get(nutrient, 0)       # progress is the combination of the recipe we are scoring, with the recipes already in meal_plan
            if len(meal_plan) > 0:                  
                for item in meal_plan.values():
                    progress += item.get('nutrition').get(nutrient, 0)
            n += 1
            i += (1 - abs(progress - goal)/goal)
    if n != 0:
        i = round(i/n, 4)
    else:
        raise ValueError("Tried to divide by 0. n is 0.")       # I don't expect this case to happen anymore
    return i

# Find the best meal that could be added to meal plan from available from recipes. Return its name.
def find_best(recipes, preferences, meal_plan):
    best = [0, None]      # i score, name
    for recipe_name, recipe_info in recipes.items():
        nutrition = recipe_info.get('nutrition', {})
        i = getImportance(nutrition, preferences, meal_plan)
        if i > best[0]:
            best[0] = i
            best[1] = recipe_name
    if best[1] is not None:     # failsafe in the event that recipes.json has less than 7 available recipes
        return best[1]
    else:
        raise TypeError("Not enough recipes available to use")

# Get the first (best) seven recipes into meal plan. This should create a decent starting point for the recursive function later on
# The originial idea was to start with a random selection of meals, but this seems like a better idea.
def initialize_meal_plan(recipes, preferences, meal_plan):
    print("Initializing Meal Plan...")
    for i in range (7):
        recipe_name = find_best(recipes, preferences, meal_plan)
        the_recipe = recipes.pop(recipe_name)
        meal_plan.update({recipe_name: the_recipe})
    print("Meal Plan Has Been Initialized.")

# this function returns the score of the current meal plan. 
# If a recipe name is passed, it returns what the score of the meal plan would be without that recipe
# filter_recipe is used after we build our initial meal plan
def get_meal_score(preferences, meal_plan, filter_recipe = None):       
    score = 0
    total_nutrients = {}        # stores total 
    for name, item in meal_plan.items():
        if name != filter_recipe:
            for nutrient, value in item.get('nutrition').items():
                if nutrient not in total_nutrients.keys():
                    total_nutrients.update({nutrient: value})
                else:
                    total_nutrients[nutrient] += value
    for nutrient in preferences.keys():
        if nutrient != 'diet':
            goal = preferences.get(nutrient)
            value = total_nutrients.get(nutrient, 0)
            score += 1 - abs(goal - value)/goal

    n = len(preferences) - 1        # -1 because we are excluding 'diet'
    if n > 0:
        score = round(score/n, 4)
    else:
        print("ERROR, n is 0 for some reason!")
    return score

# removes the recipe from meal plan, then adds it back to recipes dictionary
# finds the new best recipe. If it's the same as the removed one, then return false and add it back
def replace_recipe(recipe_name, recipes, preferences, meal_plan):
    removed = {recipe_name: meal_plan.pop(recipe_name)}
    recipes.update(removed)
    new_recipe_name = find_best(recipes, preferences, meal_plan)
    if new_recipe_name == recipe_name:
        recipes.pop(recipe_name)
        meal_plan.update(removed)
        return False
    else:
        the_recipe = recipes.pop(new_recipe_name)
        meal_plan.update({new_recipe_name: the_recipe})
        return True

# adds ingredient into the shopping list. Called by add_meal.
def add_ingredient(ingredient_name, ingredient_value):
    if ingredient_name in shopping_list:
        shopping_list[ingredient_name]['quantity'] += ingredient_value
    else:
        ingredient_unit = 'grams'   # temporary, will update to match the correct unit later
        for ingredient in ingredients:
            if ingredient.get('name') == ingredient_name:
                ingredient_unit = ingredient.get('unit')
                break
        shopping_list.update({ingredient_name: {'quantity': ingredient_value, 'unit': ingredient_unit}})

# add each ingredient to the shopping list. Calls add_ingredient.
def add_meal(meal):
    for ingredient_name, ingredient_value in meal.get('ingredients').items():
        add_ingredient(ingredient_name, ingredient_value)

# Update global variable shopping_list (a dictionary of dictionaries {chicken: {quantity: 10, unit: grams}, rice: {quantity: 20, unit: grams}...etc}
# shopping list equals total ingredients needed - ingredients we already have. Negatives should be removed
def generate_shopping_list():
    for meal in meal_plan.values():
        add_meal(meal)
    for ingredient in ingredients:
        ingredient_name = ingredient.get('name')
        ingredient_value = ingredient.get('quantity')
        if ingredient_name in shopping_list:
            shopping_list[ingredient_name]['quantity'] -= ingredient_value
            # if this creates a number that is <= 0, remove the ingredient from shopping list
            if shopping_list[ingredient_name]['quantity'] <= 0:
                shopping_list.pop(ingredient_name)



# Creates meal_plan.txt and writes helpful information into it.
def write_meal_plan(preferences, meal_plan, shopping_list):
    try:
        generate_shopping_list()
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        with open('meal_plan.txt', "w") as file:
            file.write("The Meals:\n\n")
            for day, (meal_name, meal_details) in zip(days, meal_plan.items()):
                file.write(f"{day}: {meal_name}\n")
            file.write(f"\n\nThe Meal Score: {get_meal_score(preferences, meal_plan)}")
            file.write(f"\n\nNutritional Values:")
            total_nutrients = {}        # stores total
            for name, item in meal_plan.items():
                for nutrient, value in item.get('nutrition').items():
                    if nutrient not in total_nutrients.keys():
                        total_nutrients.update({nutrient: value})
                    else:
                        total_nutrients[nutrient] += value
            for nutrient in preferences.keys():
                if nutrient != 'diet':
                    value = total_nutrients.get(nutrient, 0)
                    file.write(f"\n{nutrient}: {value}")
            file.write(f"\n\nRecipe Pool Size: {len(meal_plan) + len(recipes)}\nRecipes Used: {len(meal_plan)}\nRecipes Not Used: {len(recipes)}")
            file.write(f"\n\nRecursive Iteration Count: {recursion_count[0]}")
            file.write(f"\n\n----------------------------------\n")
            file.write(f"\n\nShopping List for the Week\n")
            for name, value in shopping_list.items():
                file.write(f"\n{name}: {value.get('quantity')} {value.get('unit')}")
    except Exception as e:
        print(f"Error writing meal plan: {e}")
        return False


# Recursively runs until the meal score satisfies our needs, or we can't improve any further.
# Each iteration must improve meal score
def improve_meal_plan(recipes, preferences, meal_plan):
    current_score = get_meal_score(preferences, meal_plan)
    if current_score >= 1 - (recursion_count[0]* 0.001):
        print("\nTHE MEAL PLAN SATISFIES PREFERENCES!\n")
        return  # meal plan is ready
    else:
        # find the recipe that has the best impact if removed
        # list all the meals and the score if they were removed. The highest score is the least important
        print(f"Trying to Improve Meal Score of {current_score}...")
        meal_scores = []
        for name, item in meal_plan.items():   
            meal_score = get_meal_score(preferences, meal_plan, name)
            meal_scores.append((name, meal_score))
        meal_scores.sort(key=lambda x: x[1], reverse=True)      # sort them in order

        # try to replace least important first. If it can't be replaced to improve the score, try the next one
        for i in range(0, len(meal_scores)):
            if replace_recipe(meal_scores[i][0], recipes, preferences, meal_plan):
                recursion_count[0] += 1
                improve_meal_plan(recipes, preferences, meal_plan)
                return
        print("Meal Plan Cannot Be Further Improved")       # can't improve anymore, so we won't recusively call again

# Plotting function 
def plot_daily_nutrition(preferences, meal_plan):
    import matplotlib.pyplot as plt

    # Extract nutrients from preferences (excluding 'diet')
    nutrients = [nutrient for nutrient in preferences.keys() if nutrient != "diet"]

    # Days of the week
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Initialize daily nutrients with all preferences nutrients set to 0
    daily_nutrients = {day: {nutrient: 0 for nutrient in nutrients} for day in days}

    # Populate daily nutrients based on the meal plan
    for day, (recipe_name, recipe) in zip(days, meal_plan.items()):
        for nutrient in nutrients:
            daily_nutrients[day][nutrient] = recipe.get('nutrition', {}).get(nutrient, 0)

    # Prepare data for plotting
    nutrient_data = {nutrient: [daily_nutrients[day][nutrient] for day in days] for nutrient in nutrients}

    # Plot the data
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

    initialize_meal_plan(recipes, preferences, meal_plan)
    improve_meal_plan(recipes, preferences, meal_plan)
    print(f"This algorithm took {recursion_count[0]} iterations to complete!")
    write_meal_plan(preferences, meal_plan,shopping_list)


    
    plot_daily_nutrition(preferences, meal_plan)

