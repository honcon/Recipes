from project10_utilities_updated import *


def close_app():
    if not db.is_closed():
        db.close()


def run_app():
    init_db()


def main():
    close_app()
    run_app()

    print("Welcome to the Recipe App!")

    while True:
        print("1. Add a Recipe")
        print("2. Search for a Recipe")
        print("3. Edit a Recipe")
        print("4. Delete a Recipe")
        print("5. Execute a Recipe")
        print("6. Exit")

        option = input("Select an option: ")

        if option == "1":
            # Add a new recipe
            recipe_name = input("Enter the recipe name: ")
            category = input("Enter the recipe category: ")
            difficulty = int(input("Enter the recipe difficulty (1-5): "))
            execution_time = int(input("Enter the recipe execution time (minutes): "))

            steps = []
            while True:
                title = input("Enter step title: ")
                description = input("Enter step description: ")
                ingredient_name = input("Enter ingredient name: ")
                ingredient_quantity = int(input("Enter ingredient quantity: "))
                number = int(input("Enter step number: "))
                step_execution_time = int(input("Enter step execution time (minutes): "))

                steps.append({
                    "title": title,
                    "description": description,
                    "ingredient_name": ingredient_name,
                    "ingredient_quantity": ingredient_quantity,
                    "number": number,
                    "step_execution_time": step_execution_time
                })

                cont = input("Do you want to add another step? (yes/no): ")
                if cont.lower() != 'yes':
                    break

            recipe_data = {
                'name': recipe_name,
                'category_name': category,
                'difficulty': difficulty,
                'execution_time': execution_time,
                'steps': steps
            }

            result = add_full_recipe(recipe_data)
            print(result["message"])

        elif option == "2":
            # Search for a recipe
            recipe_name = input("Enter the recipe name: ")
            result = search_recipe(name=recipe_name)
            if result["success"]:
                for recipe in result["recipes"]:
                    print(
                        f"ID: {recipe['id']}, Name: {recipe['name']}, Category: {recipe['category']}, Difficulty: {recipe['difficulty']}, Execution Time: {recipe['execution_time']}")
            else:
                print(result["message"])

        elif option == "3":

            # Edit a recipe

            recipe_id = int(input("Enter the recipe ID: "))

            print("What would you like to edit?")

            print("1. Recipe details")

            print("2. Steps")

            sub_option = input("Select an option: ")

            if sub_option == "1":

                updated_data = {}

                name = input("Enter new name (or press enter to skip): ")

                if name:
                    updated_data["name"] = name

                category = input("Enter new category (or press enter to skip): ")

                if category:
                    category_obj, _ = RecipeCategory.get_or_create(name=category)

                    updated_data["category"] = category_obj

                difficulty = input("Enter new difficulty (1-5) (or press enter to skip): ")

                if difficulty:
                    updated_data["difficulty"] = int(difficulty)

                execution_time = input("Enter new execution time (minutes) (or press enter to skip): ")

                if execution_time:
                    updated_data["execution_time"] = int(execution_time)

                result = edit_delete(recipe_id, action='update_recipe', updated_data=updated_data)

                print(result["message"])

            elif sub_option == "2":

                step_id = int(input("Enter the step ID: "))

                step_data = {}

                title = input("Enter new step title (or press enter to skip): ")

                if title:
                    step_data["title"] = title

                description = input("Enter new step description (or press enter to skip): ")

                if description:
                    step_data["description"] = description

                number = input("Enter new step number (or press enter to skip): ")

                if number:
                    step_data["number"] = int(number)

                step_execution_time = input("Enter new step execution time (minutes) (or press enter to skip): ")

                if step_execution_time:
                    step_data["execution_time"] = int(step_execution_time)

                result = edit_delete(recipe_id, action='update_step', step_id=step_id, step_data=step_data)

                print(result["message"])

                ingredient_data = {}

                ingredient_quantity = input("Enter new ingredient quantity (or press enter to skip): ")

                if ingredient_quantity:
                    ingredient_data["quantity"] = int(ingredient_quantity)

                result = edit_delete(recipe_id, action='update_ingredient', step_id=step_id,
                                     ingredient_data=ingredient_data)

                print(result["message"])

        elif option == "4":

            # Delete a recipe or steps

            recipe_id = int(input("Enter the recipe ID: "))

            delete_option = input("Do you want to delete the whole recipe or specific steps? (recipe/steps): ")

            if delete_option.lower() == 'recipe':

                result = edit_delete(recipe_id, action='delete_recipe')

                print(result["message"])

            elif delete_option.lower() == 'steps':

                while True:

                    step_id = int(input("Enter the step ID to delete: "))

                    result = edit_delete(recipe_id, action='delete_step', step_id=step_id)

                    print(result["message"])

                    cont = input("Do you want to delete another step? (yes/no): ")

                    if cont.lower() != 'yes':
                        break

            else:

                print("Invalid option")

                return

        elif option == "5":
            # Execute a recipe
            recipe_id = int(input("Enter the recipe ID: "))
            result = execute_recipe(recipe_id)
            if result["success"]:
                for step in result["steps"]:
                    print(
                        f"Title: {step['title']}, Description: {step['description']}, Execution Time: {step['step_execution_time']} minutes, Completion: {step['completion_percentage']}%")
            else:
                print(result["message"])

        elif option == "6":
            break


if __name__ == "__main__":
    main()
