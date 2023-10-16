import schedule
import time
import random
from datetime import datetime
from plyer import notification
# Categorized database of meals
MEAL_DATABASE = {
    'BREAKFAST': {
        'Vegan Smoothie': {
            'cuisine': 'Various',
            'diet': 'Vegan',
            'ingredients': ['banana', 'berries', 'spinach', 'almond milk'],
            'calories': 200
        },
        'Omelette': {
            'cuisine': 'Various',
            'diet': 'Non-Vegetarian',
            'ingredients': ['eggs', 'cheese', 'tomatoes', 'onions'],
            'calories': 250
        },
        # ... add more breakfast items
    },
   'LUNCH': {
    'Chicken Salad Sandwich on Whole-Wheat Bread': {
        'cuisine': 'American',
        'diet': 'Non-Vegetarian',
        'ingredients': ['chicken', 'lettuce', 'tomatoes', 'cucumbers', 'salad dressing'],
        'calories': 350
    },
    'Tuna Salad Sandwich on Whole-Wheat Bread': {
        'cuisine': 'American',
        'diet': 'Non-Vegetarian',
        'ingredients': ['tuna', 'lettuce', 'tomatoes', 'celery', 'mayonnaise'],
        'calories': 300
    },
    'Vegetarian Wrap with Hummus, Vegetables, and Cheese': {
        'cuisine': 'Various',
        'diet': 'Vegetarian',
        'ingredients': ['tortilla', 'hummus', 'vegetables', 'cheese'],
        'calories': 350
    },
    'Lentil Soup': {
        'cuisine': 'Various',
        'diet': 'Vegetarian',
        'ingredients': ['lentils', 'vegetables', 'broth'],
        'calories': 350
    },
    'Minestrone Soup': {
        'cuisine': 'Italian',
        'diet': 'Vegetarian',
        'ingredients': ['pasta', 'beans', 'vegetables', 'broth'],
        'calories': 400
    },
    'Black Bean Soup': {
        'cuisine': 'Various',
        'diet': 'Vegetarian',
        'ingredients': ['black beans', 'vegetables', 'broth'],
        'calories': 350
    },
    'Salad with Grilled Chicken or Fish': {
        'cuisine': 'Various',
        'diet': 'Non-Vegetarian',
        'ingredients': ['salad greens', 'grilled chicken or fish', 'vegetables', 'dressing'],
        'calories': 350-450
    },
    'Cobb Salad with Grilled Chicken or Fish': {
        'cuisine': 'American',
        'diet': 'Non-Vegetarian',
        'ingredients': ['salad greens', 'grilled chicken or fish', 'bacon, hard-boiled eggs, avocado, blue cheese dressing'],
        'calories': 450-500
    },
    'Leftovers from Dinner': {
        'cuisine': 'Various',
        'diet': 'Various',
        'ingredients': ['leftovers from dinner'],
        'calories': 350-500
    },
    'Hard-Boiled Eggs with Whole-Wheat Crackers and Fruit': {
        'cuisine': 'Various',
        'diet': 'Various',
        'ingredients': ['hard-boiled eggs', 'whole-wheat crackers', 'fruit'],
        'calories': 350-400
    },
    'Greek Salad with Chicken or Fish': {
        'cuisine': 'Greek',
        'diet': 'Non-Vegetarian',
        'ingredients': ['salad greens, tomatoes, cucumbers, onions, feta cheese, olives, oregano, olive oil, grilled chicken or fish'],
        'calories': 400-450
    },
    'Quinoa Salad with Vegetables and Feta Cheese': {
        'cuisine': 'Various',
        'diet': 'Vegetarian',
        'ingredients': ['quinoa', 'vegetables', 'feta cheese', 'dressing'],
        'calories': 350-400
    },
    'Chickpea Salad Sandwich on Whole-Wheat Bread': {
        'cuisine': 'Various',
        'diet': 'Vegan',
        'ingredients': ['chickpeas', 'vegetables', 'mayonnaise'],
        'calories': 300
    },
    'Chicken Caesar Salad': {
        'cuisine': 'American',
        'diet': 'Non-Vegetarian',
        'ingredients': ['salad greens, grilled chicken, Parmesan cheese, Caesar dressing'],
        'calories': 450-500
    },
    'Cobb Salad with Quinoa and Tofu': {
        'cuisine': 'American',
        'diet': 'Vegetarian',
        'ingredients': ['quinoa', 'vegetables', 'tofu', 'dressing'],
        'calories': 350-400
    },
    'Tofu Stir-Fry with Brown Rice': {
        'cuisine': 'Asian',
        'diet': 'Vegetarian',
        'ingredients': ['tofu', 'broccoli', 'carrots', 'bell peppers', 'soy sauce', 'ginger'],
   'calories': 350-400
    },
}
    
    }
    


# Function to suggest a meal
def suggest_meal(meal_type):
    meal = random.choice(list(MEAL_DATABASE[meal_type].keys()))
    details = MEAL_DATABASE[meal_type][meal]
    message = f"It's {meal_type.lower()} time!\nHow about some {meal}?\nCuisine: {details['cuisine']}\nIngredients: {', '.join(details['ingredients'])}\nCalories: {details['calories']}"
    notification.notify(
        title=f"{meal_type} Meal Suggestion",
        message=message,
        timeout=10
    )

# Scheduling meal suggestions
schedule.every().day.at("15:15").do(suggest_meal, 'BREAKFAST')  # Suggest breakfast at 8:00 AM
schedule.every().day.at("15:17").do(suggest_meal, 'LUNCH')      # Suggest lunch at 12:00 PM
schedule.every().day.at("15:18").do(suggest_meal, 'DINNER')     # Suggest dinner at 7:00 PM

while True:
    schedule.run_pending()
    time.sleep(1)
