from backend import db
from backend import utilities
import pprint

db.init_db()

recipe_data = {
    'name': 'Carbonara 2',
    'category': 'Pasta',
    'difficulty': 2,
    'execution_time': 20,  # in minutes
    'steps': [
        {
            'title': 'Prepare Ingredients',
            'description': 'Measure all the ingredients.',
            'number': 1,
            'execution_time': 5,
            'ingredients': ['Avga', 'Ntomates', 'Kreas']
        },
        {
            'title': 'Cook Pasta',
            'description': 'Boil water and cook pasta.',
            'number': 2,
            'execution_time': 10,
            'ingredients': ['Patates', 'Ladi', 'Alati']
        }
    ]
}

# result = utilities.add_full_recipe(recipe_data)
result = utilities.get_full_recipe(2)
pprint.pprint(result)
# ing = list(db.Ingredient.select())
