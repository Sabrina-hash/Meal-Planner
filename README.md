# Meal Planner Project
This project is a meal planning application that recommends recipes,
creates meal plans, generates shopping lists, and provides nutritional
analysis.
## Setup
1. Clone the repository
2. Install the required packages:
`pip install -r requirements.txt`.
`pip install matplotlib` works as well
4. Ensure you have 'ingredients.csv', 'recipies.json', and 'preferences.json' in the
project directory
5. Run the main script:
`python myProject.py`
## Running Tests
To run the unit tests:
`python -m unittest unit_test.test_myProject`
## Features
- Recipe recommendation based on available ingredients and dietary
preferences
- Weekly meal plan generation
- Shopping list creation
- Nutritional analysis of the meal plan
- No duplicate meals
- Very Fast Runtime
## File Structure
- `myProject.py`: Main script containing all functions
- `test_myProject.py`: Test script containing several test cases for the methods in `myProject.py`. Located in the `unit_tests` directory
- `ingredients.csv`: CSV file containing available ingredients. Any number of ingredients can be added in the format name,quantity,unit.
- `preferences.json`: JSON file containing user preferences and
nutritional goals. Must be in the same format as provided. Any number of nutrients can be added or removed.
- `recipes.json`: JSON file containing recipes, their ingredients, dietary restriction, and nutritional values. Any number of recipes can be added or removed as long as it follows the same format.
- `requirements.txt`: List of required Python packages. It's just matplotlib.
- `test_myProject.py`: Unit tests for the project
