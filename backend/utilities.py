from backend.db import *
from peewee import IntegrityError
from backend.initial_recipes import recipes as initial_recipes

init_db()


def add_full_recipe(recipe_data):
    try:
        with db.atomic():
            category, _ = RecipeCategory.get_or_create(name=recipe_data['category'])

            recipe = Recipe.create(
                name=recipe_data['name'],
                category=category,
                difficulty=recipe_data['difficulty'],
                execution_time=recipe_data['execution_time']
            )

            for step_data in recipe_data['steps']:
                step = Step.create(
                    recipe_id=recipe,
                    title=step_data['title'],
                    description=step_data['description'],
                    number=step_data['number'],
                    execution_time=step_data['execution_time']
                )
                
                for ingredient_name in step_data['ingredients']:
                    ingredient, _ = Ingredient.get_or_create(name=ingredient_name)
                    RecipesIngredients.create(
                        recipe_id=recipe,
                        ingredient_id=ingredient,
                        step_id=step
                    )

        return {"success": True, "message": "Recipe and details added successfully."}

    except IntegrityError as e:
        return {"success": False, "message": f"Database error: {e}"}

    except Exception as e:
        return {"success": False, "message": f"Error: {e}"}


def get_full_recipe(recipe_id):
    try:
        recipe = Recipe.get_by_id(recipe_id)
        recipe_data = {
            "id": recipe.id,
            "name": recipe.name,
            "category": recipe.category.name,
            "difficulty": recipe.difficulty,
            "execution_time": recipe.execution_time,
            "steps": []
        }

        steps = (Step.select().where(Step.recipe_id == recipe_id).order_by(Step.number))

        for step in steps:
            step_data = {
                "id": step.id,
                "title": step.title,
                "description": step.description,
                "number": step.number,
                "execution_time": step.execution_time,
                "ingredients": []
            }

            ingredients = (RecipesIngredients.select().where(RecipesIngredients.step_id == step.id))

            for ingredient in ingredients:
                step_data["ingredients"].append({
                    "id": ingredient.ingredient_id.id,
                    "name": ingredient.ingredient_id.name,
                    "quantity": ingredient.quantity
                })

            recipe_data["steps"].append(step_data)

        return {"success": True, "recipe": recipe_data}

    except Recipe.DoesNotExist:
        return {"success": False, "message": "Recipe does not exist."}

    except Exception as e:
        return {"success": False, "message": f"Error: {e}"}


def delete_recipe(recipe_id):
    try:
        recipe = Recipe.get_by_id(recipe_id)
        recipe.delete_instance(recursive=True)
        return {"success": True, "message": "Recipe deleted successfully."}

    except Recipe.DoesNotExist:
        return {"success": False, "message": "Recipe does not exist."}

    except Exception as e:
        return {"success": False, "message": f"Error: {e}"}


def update_recipe(recipe_id, updated_data):
    try:
        with db.atomic():
            recipe = Recipe.get_by_id(recipe_id)
            recipe.delete_instance(recursive=True)

            category, _ = RecipeCategory.get_or_create(name=updated_data['category'])

            recipe = Recipe.create(
                id=recipe_id,
                name=updated_data['name'],
                category=category,
                difficulty=updated_data['difficulty'],
                execution_time=updated_data['execution_time']
            )

            for step_data in updated_data['steps']:
                step = Step.create(
                    recipe_id=recipe,
                    title=step_data['title'],
                    description=step_data['description'],
                    number=step_data['number'],
                    execution_time=step_data['execution_time']
                )
                
                for ingredient_name in step_data['ingredients']:
                    ingredient, _ = Ingredient.get_or_create(name=ingredient_name)
                    RecipesIngredients.create(
                        recipe_id=recipe,
                        ingredient_id=ingredient,
                        step_id=step
                    )

        return {"success": True, "message": "Recipe updated successfully."}

    except Recipe.DoesNotExist:
        return {"success": False, "message": "Recipe does not exist."}

    except Exception as e:
        return {"success": False, "message": f"Error: {e}"}


def search_recipe(search_term=None, category=None):
    try:

        query = Recipe.select()

        if search_term:
            query = query.where(Recipe.name.contains(search_term))

        if category:
            query = query.join(RecipeCategory).where(RecipeCategory.name.contains(category))

        recipes = list(query)

        if recipes:
            return {"success": True, "recipes": recipes}

        else:
            return {"success": False, "message": "No recipes found."}

    except Exception as e:
        return {"success": False, "message": f"Error: {e}"}


def get_categories():
    categories = list(RecipeCategory.select())
    return {category.id: category.name for category in categories}


def get_ingredients():
    ingredients = list(Ingredient.select())
    return {ingredient.id: ingredient.name for ingredient in ingredients}


def delete_ingredient(ingredient_id):
    try:
        Ingredient.delete().where(Ingredient.id == ingredient_id).execute()
        return {"success": True, "message": "Ingredient deleted successfully."}

    except Ingredient.DoesNotExist:
        return {"success": False, "message": "Ingredient does not exist."}

    except Exception as e:
        return {"success": False, "message": f"Error: {e}"}


def add_ingredient(ingredient_name):
    try:
        ingredient = Ingredient.create(name=ingredient_name)
        return {"success": True, "message": "Ingredient added successfully.", "ingredient_id": ingredient.id}

    except IntegrityError as e:
        return {"success": False, "message": f"Database error: {e}"}

    except Exception as e:
        return {"success": False, "message": f"Error: {e}"}


recipes = Recipe.select()

if recipes.count() == 0:
    for recipe in initial_recipes():
        add_full_recipe(recipe)
