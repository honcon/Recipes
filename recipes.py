import tkinter as tk
from backend import utilities
from tkinter import ttk, simpledialog, messagebox
from add_edit_recipe import AddEditRecipe
from execution import Execution

class Recipes(tk.Frame):

    def load_recipes(self, search_term=None, category=None):

        response = utilities.search_recipe(search_term=search_term, category=category)

        if response["success"]:
            recipes = response["recipes"]
        else:
            recipes = []

        self.recipes_table.delete(*self.recipes_table.get_children())

        for recipe in recipes:
            self.recipes_table.insert("", "end", values=(recipe.id, recipe.name))


    def load_categories(self):
        categories = list(utilities.get_categories().values())

        self.categories = ["Όλες οι κατηγορίες"] + categories
        self.category_select["values"] = self.categories

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.parent = parent
        self.selected_recipe = tk.IntVar()

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.search_recipes)
        self.categories = []

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

        self.execute_recipe_button = tk.Button(button_frame, text="Εκτέλεση", command=lambda: self.execute_recipe(self.selected_recipe.get()))
        self.execute_recipe_button.grid(row=0, column=2, sticky="w")
        self.execute_recipe_button.config(state="disabled")

        self.search_entry = tk.Entry(self.heading, textvariable=self.search_var)
        self.search_entry.grid(row=1, column=1, sticky="e")

        self.category_select = ttk.Combobox(self.heading, state="readonly")
        self.category_select.grid(row=2, column=0, columnspan=2, sticky="e")
        self.category_select.bind("<<ComboboxSelected>>", lambda e: self.search_recipes())

        self.heading.pack(fill="x")

        self.recipes_table = ttk.Treeview(self, columns=("id", "name"), selectmode="browse", show='headings')
        self.recipes_table["displaycolumns"] = ["name"]
        self.recipes_table.heading("name", text="Συνταγή")
        self.recipes_table.column("name", width=200)
        self.recipes_table.pack(fill="both", expand=True)
        self.recipes_table.bind("<<TreeviewSelect>>", self.select_recipe)

        self.load_categories()
        self.category_select.current(0)

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


    def search_recipes(self, *args):
        category_term = self.category_select.current() > 0 and self.categories[self.category_select.current()] or None
        category_name = self.categories[self.category_select.current()]

        if (self.search_var.get() == ""):
            self.recipes_table.heading("name", text=f"Συνταγή {category_term and f'({category_name})' or ''}")
            self.load_recipes(category=category_term)
        else:
            self.recipes_table.heading("name", text=f"Αναζήτηση για {self.search_var.get()} {category_term and f'σε ({category_name})' or ''}")
            self.load_recipes(self.search_var.get(), category_term)

    def open_add_edit_recipe(self, recipe_id=None):

        add_recipe = AddEditRecipe(self, recipe_id=recipe_id)

        add_recipe.minsize(900, 400)
        add_recipe.resizable(True, True)

        x = self.parent.winfo_x() + self.parent.winfo_width() // 2 - 900 // 2
        y = self.parent.winfo_y() + self.parent.winfo_height() // 2 - 400 // 2
        add_recipe.geometry("+{}+{}".format(x, y))

        add_recipe.transient(self)
        add_recipe.grab_set()
        self.wait_window(add_recipe)


    def execute_recipe(self, recipe_id):
        execution = Execution(self, recipe_id=recipe_id)

        execution.minsize(700, 500)
        execution.resizable(True, True)

        x = self.parent.winfo_x() + self.parent.winfo_width() // 2 - 700 // 2
        y = self.parent.winfo_y() + self.parent.winfo_height() // 2 - 500 // 2
        execution.geometry("+{}+{}".format(x, y))

        execution.transient(self)
        execution.grab_set()
        self.wait_window(execution)

    def add_recipe(self):
        self.open_add_edit_recipe()

    def delete_recipe(self):
        result = messagebox.askyesno("Διαγραφή", f"Είστε σίγουροι ότι θέλετε να διαγράψετε τη συνταγή με id:{self.selected_recipe.get()};", parent=self)
        if result:
            response = utilities.delete_recipe(self.selected_recipe.get())

            if response["success"]:
                self.load_recipes()
            else:
                messagebox.showerror("Σφάλμα", response["message"], parent=self)


    def edit_recipe(self):
        self.open_add_edit_recipe(recipe_id=self.selected_recipe.get())
