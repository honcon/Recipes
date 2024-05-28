# /Library/Frameworks/Python.framework/Versions/3.12/bin/python3

import tkinter as tk

from ingredients import Ingredients
from recipes import Recipes


class App(tk.Tk):
    menu_type = {"recipes": 0, "ingredients": 1}
    selected_menu = None

    def __init__(self):
        super().__init__()

        self.geometry("800x600")
        self.minsize(800, 600)
        self.resizable(True, True)
        self.title("Συνταγες Μαγειρικης")

        leftbar = tk.Frame(self, border=0, relief="solid", padx=10, pady=10)
        leftbar.pack(fill="y", side="left", expand=False)

        recipes_button = tk.Button(leftbar, text="Συνταγές", width=15, command=lambda: self.set_menu(self.menu_type["recipes"]))
        recipes_button.pack()

        ingredients_button = tk.Button(leftbar, text="Υλικά", width=15, command=lambda: self.set_menu(self.menu_type["ingredients"]))
        ingredients_button.pack()

        credits = tk.Label(leftbar, text="ΠΛΗΠΡΟ Τελική εργασία\n\nΔημιουργήθηκε από τούς:\nΔημήτρη Κωνσταντακόπουλο,\nΚωνσταντίνο Χονδρό\n\nΣυντονιστής έργου:\nΔημήτρης Κωνσταντακόπουλος", font=("Arial", 9, 'bold'), fg="gray")
        credits.pack(side="bottom")

        mainframe = tk.Frame(self, border=0, relief="solid", padx=10, pady=10)
        mainframe.pack(fill="both", side="left", expand=True)

        self.recipes = Recipes(self)
        self.ingredients = Ingredients(self)

        self.recipes.place(in_=mainframe, x=0, y=0, relwidth=1, relheight=1)
        self.ingredients.place(in_=mainframe, x=0, y=0, relwidth=1, relheight=1)

        # Define Recipes as the default menu
        self.recipes.lift()

    def set_menu(self, menu):
        self.selected_menu = menu

        if self.selected_menu == self.menu_type["recipes"]:
            self.recipes.lift()
        if self.selected_menu == self.menu_type["ingredients"]:
            self.ingredients.lift()


if __name__ == '__main__':
    app = App()
    app.mainloop()
