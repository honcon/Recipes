import tkinter as tk


class AddEditRecipe(tk.Toplevel):

    def __init__(self, parent, recipe_id, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        
        self.edit_mode = recipe_id and recipe_id > 0
        
        self.title(f"Επεξεργασία Συνταγής {recipe_id}" if self.edit_mode else "Δημιουργία")

        self.label = tk.Label(self, text="Επεξεργασία" if self.edit_mode else "Δημιουργία", font=("Arial", 24))

        self.label.pack(fill="x")
