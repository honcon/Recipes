import tkinter as tk
from backend import project10_db as db
from tkinter import ttk


class Ingredients(tk.Frame):
    def __init__(self, *args, **kwargs):

        ingredients = list(db.Ingredient.select())

        tk.Frame.__init__(self, *args, **kwargs)
        self.label = tk.Label(self, text="Ingredients", font=("Arial", 24), border=1, relief="solid", padx=10, pady=10)
        self.label.pack(fill="x")

        ingredients_table = ttk.Treeview(self, columns=("name"), selectmode="browse", show='headings')
        ingredients_table.heading("name", text="Name")
        ingredients_table.column("name", width=200)
        ingredients_table.pack(fill="both", expand=True)

        for ingredient in ingredients:
            ingredients_table.insert("", "end", values=(ingredient.name))

