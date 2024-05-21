import tkinter as tk
from backend import project10_db as db
from tkinter import ttk, simpledialog


class Recipes(tk.Frame):

    def load_recipes(self, search_term=None):
        if search_term:
            recipes = list(db.Recipe.select().where(db.Recipe.name.contains(search_term)))
        else:
            recipes = list(db.Recipe.select())

        self.recipes_table.delete(*self.recipes_table.get_children())

        for recipe in recipes:
            self.recipes_table.insert("", "end", values=(recipe.id, recipe.name))

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.selected_recipe = tk.IntVar()

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.search_recipes)

        self.heading = tk.Frame(self)
        self.heading.columnconfigure(0, weight=1)
        self.heading.rowconfigure(0, weight=1)

        self.label = tk.Label(self.heading, text="Συνταγές", font=("Arial", 24))
        self.label.grid(row=0, column=0, sticky="w")

        self.add_recipe_button = tk.Button(self.heading, text="Προσθήκη", command=self.add_recipe)
        self.add_recipe_button.grid(row=0, column=1, sticky="e")

        button_frame = tk.Frame(self.heading)
        button_frame.grid(row=1, column=0, sticky="w")

        self.delete_recipe_button = tk.Button(button_frame, text="Διαγραφή", command=self.delete_recipe)
        self.delete_recipe_button.grid(row=0, column=0, sticky="w")
        self.delete_recipe_button.config(state="disabled")

        self.edit_recipe_button = tk.Button(button_frame, text="Επεξεργασία", command=self.edit_recipe)
        self.edit_recipe_button.grid(row=0, column=1, sticky="w")
        self.edit_recipe_button.config(state="disabled")

        self.execute_recipe_button = tk.Button(button_frame, text="Εκτέλεση", command=self.execute_recipe)
        self.execute_recipe_button.grid(row=0, column=2, sticky="w")
        self.execute_recipe_button.config(state="disabled")

        self.search_entry = tk.Entry(self.heading, textvariable=self.search_var)
        self.search_entry.grid(row=1, column=1, sticky="e")


        self.heading.pack(fill="x")

        self.recipes_table = ttk.Treeview(self, columns=("id", "name"), selectmode="browse", show='headings')
        self.recipes_table["displaycolumns"] = ["name"]
        self.recipes_table.heading("name", text="Συνταγή")
        self.recipes_table.column("name", width=200)
        self.recipes_table.pack(fill="both", expand=True)
        self.recipes_table.bind("<<TreeviewSelect>>", self.select_recipe)

        self.load_recipes()

    def select_recipe(self, event):
        try:
            item = self.recipes_table.selection()[0]
            self.selected_recipe.set(self.recipes_table.item(item)["values"][0])
            self.delete_recipe_button.config(state="normal")
            self.edit_recipe_button.config(state="normal")
            self.execute_recipe_button.config(state="normal")
        except IndexError:
            self.selected_recipe.set(0)
            self.delete_recipe_button.config(state="disabled")
            self.edit_recipe_button.config(state="disabled")
            self.execute_recipe_button.config(state="disabled")


    def search_recipes(self, var, index, mode):
        if (self.search_var.get() == ""):
            self.recipes_table.heading("name", text="Συνταγή")
            self.load_recipes()
        else:
            self.recipes_table.heading("name", text="Αναζήτηση για {}".format(self.search_var.get()))
            self.load_recipes(self.search_var.get())


    def add_recipe(self):
        pass

    def delete_recipe(self):
        pass

    def edit_recipe(self):
        pass

    def execute_recipe(self):
        pass