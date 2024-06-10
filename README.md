# Recipes App

Overview

The Recipes application is a Windows-based executable that allows users to manage and execute cooking recipes. No Python installation is required to use the application. The key functionalities include adding, editing, storing, executing, and deleting recipes, as well as managing ingredients.
Installation and Usage
Prerequisites

    Windows Operating System

Steps to Run the Application

    Download the Application:
        Download the executable file named Recipes.exe to your preferred folder.

    Run the Application:
        Locate the Recipes.exe file in your chosen folder.
        Double-click the icon, or right-click the icon and select "Open", or select the icon and press "Enter" on the keyboard.

    Initial Setup:
        On the first run, a database file named recipes.db will be created if it does not already exist.
        The main application window will open, providing access to all necessary features.

Features
Preloaded Recipes

    The application includes three preloaded recipes with the necessary ingredients.

Adding and Managing Ingredients

    View Ingredients:
        Click on "Υλικά" to view existing ingredients.
    Add Ingredient:
        Click "Προσθήκη", enter the ingredient name in the new window, and confirm with "OK" or "Enter". Cancel with "Cancel" or "Χ".
    Delete Ingredient:
        Select an ingredient from the list and click "Διαγραφή" to remove it from the database.

Adding and Managing Recipes

    Add Recipe:
        Click "Προσθήκη" from the main menu.
        Enter the recipe name, select or create a category, and set the difficulty level (Easy, Medium, Hard).
        Add at least one step to save the recipe.
    Recipe Steps:
        For each step, provide a title, execution time (hours and minutes), select and add necessary ingredients from the drop-down list, and write a brief description.
        To delete a step, click "Διαγραφή Βήματος".
        The total preparation time is calculated based on the time required for each step.
    Save Recipe:
        Click "Αποθήκευση" to save the new recipe. A confirmation message will appear.
    Edit Recipe:
        Select a recipe from the list, click "Επεξεργασία", and make changes as needed.
    Delete Recipe:
        Select a recipe and click "Διαγραφή" to remove it permanently from the database.

Executing Recipes

    Execute Recipe:
        Select a recipe and click "Εκτέλεση" to follow step-by-step instructions.
        View required ingredients, execution time, and step descriptions.
        Navigate through steps using "Επόμενο" and "Προηγούμενο".
        On completion, a message will notify the user. Close the execution window with "Χ".

Searching Recipes

    Use the search field above "Όλες οι κατηγορίες" to find a recipe by name or category.

Developer Instructions
Development Environment

    Language: Python 3.12.3
    Libraries Used: tkinter
    Packages Used: tkscrolledframe, peewee

Setting Up the Development Environment

    Install Required Packages:
        Open a Windows console and run:

            `pip3 install peewee`
            `pip3 install tkscrolledframe`

Database Management:

    It is recommended to install and use "DB Browser (SQLite)" to read and edit the recipes.db file.
    
    Download from: https://sqlitebrowser.org/dl/