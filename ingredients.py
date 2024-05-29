import tkinter as tk
from backend import utilities
from tkinter import ttk, simpledialog, messagebox


class Ingredients(tk.Frame):

    def load_ingredients(self):
        ingredients = utilities.get_ingredients()
        # clear the table and fill it with the new data
        self.ingredients_table.delete(*self.ingredients_table.get_children())
        
        for ingredient_id, ingredient_name in ingredients.items():
            self.ingredients_table.insert("", "end", values=(ingredient_id, ingredient_name))

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.selected_ingredient = tk.IntVar()

        self.heading = tk.Frame(self)
        self.heading.columnconfigure(0, weight=1)

        self.heading_label = tk.Label(self.heading, text="Υλικά", font=("Arial", 24))
        self.heading_label.grid(row=0, column=0, sticky="w")

        self.add_ingredient_button = tk.Button(self.heading, text="Προσθήκη", command=self.add_ingredient)
        self.add_ingredient_button.grid(row=0, column=1, sticky="e")

        self.delete_ingredient_button = tk.Button(self.heading, text="Διαγραφη", command=self.delete_ingredient)
        self.delete_ingredient_button.grid(row=0, column=3, sticky="e")
        self.delete_ingredient_button.config(state="disabled")

        self.heading.pack(fill="x")

        self.ingredients_table = ttk.Treeview(self, columns=("id", "name"), selectmode="browse", show='headings')
        self.ingredients_table["displaycolumns"] = ["name"]
        self.ingredients_table.heading("name", text="Υλικό")
        self.ingredients_table.column("name", width=200)
        self.ingredients_table.pack(fill="both", expand=True)
        self.ingredients_table.bind("<<TreeviewSelect>>", self.select_ingredient)

        self.load_ingredients()

    def select_ingredient(self, event):
        try:
            item = self.ingredients_table.selection()[0]
            self.selected_ingredient.set(self.ingredients_table.item(item)["values"][0])
            self.delete_ingredient_button.config(state="normal")
        except IndexError:
            self.selected_ingredient.set(0)
            self.delete_ingredient_button.config(state="disabled")

    def add_ingredient(self):
        new_ingredient = simpledialog.askstring("Προσθήκη Υλικού", "Όνομα Υλικού", parent=self)

        # new ingredient is not None or empty string
        if new_ingredient:
            response = utilities.add_ingredient(new_ingredient)

            if response["success"]:
                self.load_ingredients()
            else:
                messagebox.showerror("Σφάλμα", response["message"], parent=self)

    def delete_ingredient(self):
        if self.selected_ingredient:
            response = utilities.delete_ingredient(self.selected_ingredient.get())

            if response["success"]:
                self.load_ingredients()
            else:
                messagebox.showerror("Σφάλμα", response["message"])