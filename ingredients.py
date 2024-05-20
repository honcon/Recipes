import tkinter as tk
from backend import project10_db as db
from tkinter import ttk, simpledialog

class Ingredients(tk.Frame):
    
    selected_ingredient = None

    def load_ingredients(self):
        ingredients = list(db.Ingredient.select())
        # clear the table and fill it with the new data
        self.ingredients_table.delete(*self.ingredients_table.get_children())
        
        for ingredient in ingredients:
            self.ingredients_table.insert("", "end", values=(ingredient.id, ingredient.name))


    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.heading = tk.Frame(self)

        self.heading.columnconfigure(0, weight=1)
        self.heading.columnconfigure(1, weight=1)

        self.heading_label = tk.Label(self.heading, text="Υλικά", font=("Arial", 24))
        self.heading_label.grid(row=0, column=0, sticky="w")

        self.add_ingredient_button = tk.Button(self.heading, text="Προσθήκη Υλικού", command=self.add_ingredient)
        self.add_ingredient_button.grid(row=0, column=1, sticky="e")

        self.heading.pack(fill="x")



        self.ingredients_table = ttk.Treeview(self, columns=("id", "name"), selectmode="browse", show='headings')
        self.ingredients_table["displaycolumns"] = ["name"]
        self.ingredients_table.heading("name", text="Υλικό")
        self.ingredients_table.column("name", width=200)
        self.ingredients_table.pack(fill="both", expand=True)
        self.ingredients_table.bind("<<TreeviewSelect>>", self.select_ingredient)

        self.load_ingredients()

    def select_ingredient(self, event):
        item = self.ingredients_table.selection()[0]
        self.selected_ingredient = self.ingredients_table.item(item)["values"][0]

    def add_ingredient(self):
        new_ingredient = simpledialog.askstring("Προσθήκη Υλικού", "Όνομα Υλικού", parent=self)

        # new ingredient is not None or empty string
        if new_ingredient:
            db.Ingredient.create(name=new_ingredient)
            self.load_ingredients()