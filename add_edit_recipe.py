import tkinter as tk
from backend import db, utilities
from tkinter import messagebox, ttk
from tkscrolledframe import ScrolledFrame
from pprint import pprint
# https://pythonassets.com/posts/drop-down-list-combobox-in-tk-tkinter/

class StepFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent.steps_frame, *args, **kwargs, bd=2, relief="raised")

        self.step_number = tk.IntVar()
        self.title = tk.StringVar(value=kwargs.get("title", ""))
        self.description = tk.StringVar(value=kwargs.get("description", ""))
        self.execution_time = tk.IntVar(value=kwargs.get("execution_time", 0))
        self.execution_time.trace_add("write", lambda *args: parent.calculate_execution_time())

        self.ingredients_list = parent.ingredients_list
        self.selected_ingredient = tk.IntVar()

        self.pack(fill="x", expand=True)

        head_frame = tk.Frame(self, padx=10, pady=10)
        head_frame.columnconfigure(1, weight=1)
        step_label = tk.Label(head_frame, text="Βήμα", font=("Helvetica", 13, "bold"), anchor="w")
        step_label_number = tk.Label(head_frame, textvariable=self.step_number, anchor="w")

        step_label.grid(row=0, column=0, sticky="w")
        step_label_number.grid(row=0, column=1, sticky="w")

        delete_button = tk.Button(head_frame, text="Διαγραφή Βήματος", command=lambda: parent.delete_step(self))
        delete_button.grid(row=0, column=2, sticky="e")
        
        head_frame.pack(fill="x", expand=True)
        separator = ttk.Separator(self, orient="horizontal") 
        separator.pack(fill="x", padx=10)
        

    # Title

        title_frame = tk.Frame(self, padx=10, pady=10)
        title_frame.grid_columnconfigure(1, weight=1)

        title_label = tk.Label(title_frame, text="Τίτλος", font=("Helvetica", 12, "bold"), width=20, anchor="e")
        title_label.grid(row=0, column=0, sticky="w")

        title_entry = tk.Entry(title_frame, textvariable=self.title)
        title_entry.grid(row=0, column=1, sticky="we")

        title_frame.pack(fill="x", expand=True)

    # Execution Time in hours and minutes
        time_frame = tk.Frame(self, padx=10, pady=10)
        time_frame.grid_columnconfigure(5, weight=1)

        time_label = tk.Label(time_frame, text="Χρόνος Εκτέλεσης", font=("Helvetica", 12, "bold"), width=20, anchor="e")
        time_label.grid(row=0, column=0, sticky="w")


        self.time_entry_hours = tk.Entry(time_frame, width=3)
        self.time_entry_hours.grid(row=0, column=1, sticky="w")
        self.time_entry_hours.bind("<KeyRelease>", self.on_update_hours)

        label_hours = tk.Label(time_frame, text="Ώρες", font=("Helvetica", 12))
        label_hours.grid(row=0, column=2, sticky="w")

        self.time_entry_minutes = tk.Entry(time_frame, width=3)
        self.time_entry_minutes.grid(row=0, column=3, sticky="w")
        self.time_entry_minutes.bind("<KeyRelease>", self.on_update_minutes)

        label_minutes = tk.Label(time_frame, text="Λεπτά", font=("Helvetica", 12))
        label_minutes.grid(row=0, column=4, sticky="w")

        time_frame.pack(fill="x", expand=True)


    # Ingredients

        ingredients_frame = tk.Frame(self, padx=10, pady=10)
        ingredients_frame.grid_columnconfigure(1, weight=1)

        ingredients_label = tk.Label(ingredients_frame, text="Υλικά", font=("Helvetica", 12, "bold"), width=20, anchor="e")
        ingredients_label.grid(row=1, column=0, sticky="w")
        
        ingredients_top_bar = tk.Frame(ingredients_frame)
        ingredients_top_bar.grid(row=0, column=1, sticky="we")
        ingredients_top_bar.grid_columnconfigure(2, weight=1)

        self.ingredient_list = ttk.Combobox(ingredients_top_bar, state="readonly", values=list(self.ingredients_list.values()))
        self.ingredient_list.bind("<<ComboboxSelected>>", self.on_change_ingredient_from_list)
        self.ingredient_list.grid(row=0, column=0, sticky="w")


        self.add_ingredient_button = tk.Button(ingredients_top_bar, text="Προσθήκη", command=self.add_ingredient)
        self.add_ingredient_button.grid(row=0, column=1, sticky="w")
        self.add_ingredient_button.config(state="disabled")
        
        self.delete_ingredient_button = tk.Button(ingredients_top_bar, text="Διαγραφή Υλικού", command=self.delete_ingredient)
        self.delete_ingredient_button.grid(row=0, column=2, sticky="e")
        self.delete_ingredient_button.config(state="disabled")

        self.ingredients_table = ttk.Treeview(ingredients_frame, columns=("id", "name"), selectmode="browse", show='headings', height=5)
        self.ingredients_table["displaycolumns"] = ["name"]
        self.ingredients_table.heading("name", text="Υλικό")
        self.ingredients_table.column("name", width=200)
        self.ingredients_table.grid(row=1, column=1, sticky="we")
        self.ingredients_table.bind("<<TreeviewSelect>>", self.select_ingredient)

        ingredients_frame.pack(fill="x", expand=True)

    # Description

        description_frame = tk.Frame(self, padx=10, pady=10)
        description_frame.grid_columnconfigure(1, weight=1)

        description_label = tk.Label(description_frame, text="Περιγραφή", font=("Helvetica", 12, "bold"), width=20, anchor="e")
        description_label.grid(row=0, column=0, sticky="w")

        description_entry = tk.Text(description_frame, height=10, width=30)
        description_entry.insert(tk.END, self.description.get())

        description_entry.bind("<KeyRelease>", lambda e: self.description.set(description_entry.get("1.0", tk.END)))

        description_entry.grid(row=0, column=1, sticky="we")

        description_frame.pack(fill="x", expand=True)

    def on_change_ingredient_from_list(self, e):
        if self.ingredient_list.get():
            self.add_ingredient_button.config(state="normal")

    def select_ingredient(self, event):
        try:
            item = self.ingredients_table.selection()[0]
            self.selected_ingredient.set(self.ingredients_table.item(item)["values"][0])
            self.delete_ingredient_button.config(state="normal")
        except IndexError:
            self.selected_ingredient.set(0)
            self.delete_ingredient_button.config(state="disabled")

    def add_ingredient(self):
        ingredient_name = self.ingredient_list.get()
        ingredient_id = list(self.ingredients_list.keys())[list(self.ingredients_list.values()).index(ingredient_name)]

        self.ingredient_list.set("")
        self.add_ingredient_button.config(state="disabled")
        self.ingredients_table.insert("", "end", values=(ingredient_id, ingredient_name))

    def delete_ingredient(self):
        selection = self.ingredients_table.selection()
        if selection:
            self.ingredients_table.delete(selection)


    def on_update_hours(self, e):
        value = self.time_entry_hours.get()

        if not value.isdigit() or not 0 <= int(value) <= 99:
            self.time_entry_hours.delete(0, tk.END)

        self.update_time()


    def on_update_minutes(self, e):
        value = self.time_entry_minutes.get()

        if not value.isdigit() or not 0 <= int(value) <= 59:
            self.time_entry_minutes.delete(0, tk.END)

        self.update_time()


    def update_time(self):
        total_minutes = int(self.time_entry_hours.get() or 0) * 60 + int(self.time_entry_minutes.get() or 0)
        self.execution_time.set(total_minutes)

class AddEditRecipe(tk.Toplevel):

    def __init__(self, parent, recipe_id, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        
        self.edit_mode = recipe_id and recipe_id > 0
        self.parent = parent

        self.categories = self.get_categories()
        self.ingredients_list = self.get_ingredients()


        self.name = tk.StringVar()
        self.execution_time = tk.IntVar()
        self.difficulty = tk.IntVar() # 1: easy, 2: medium, 3: hard
        self.category = tk.StringVar()

        self.execution_time.trace_add("write", lambda *args: self.update_time())

        self.steps = []

        self.title(f"Επεξεργασία Συνταγής {recipe_id}" if self.edit_mode else "Δημιουργία")

        top_bar = tk.Frame(self, padx=10, pady=10)
        top_bar.columnconfigure(0, weight=1)

        label_container = tk.Frame(top_bar)
        label_container.grid(row=0, column=0, sticky="w")

        self.label = tk.Label(label_container, text="Επεξεργασία συνταγής: " if self.edit_mode else "Νέα συνταγή: ", font=("Arial", 24))
        self.label_name = tk.Label(label_container, textvariable=self.name, font=("Arial", 24))

        self.label.grid(row=0, column=0, sticky="w")
        self.label_name.grid(row=0, column=1)

        self.save_button = tk.Button(top_bar, text="Αποθήκευση", command=self.save)
        self.save_button.grid(row=0, column=1, sticky="e")

        top_bar.pack(fill="x")
        
        left_frame = tk.Frame(self, padx=5, pady=5, border=0, relief="solid", width=200)
        main_frame = tk.Frame(self, padx=5, pady=5, border=0, relief="solid")

        left_frame.pack(side="left", fill="y", expand=False)
        main_frame.pack(fill="both", side="left", expand=True)


    # Basic Recipe Information

        self.recipe_name_label = tk.Label(left_frame, text="Όνομα Συνταγής", anchor="w", font=("Helvetica", 13, "bold"))
        self.recipe_name_label.pack(fill="x")

        self.recipe_name = tk.Entry(left_frame, textvariable=self.name)
        self.recipe_name.pack(fill="x")

        self.recipe_category_label = tk.Label(left_frame, text="Κατηγορία", anchor="w", font=("Helvetica", 13, "bold"))
        self.recipe_category_label.pack(fill="x")

        self.recipe_category = ttk.Combobox(left_frame, values=self.categories)
        self.recipe_category.pack(fill="x")

        self.recipe_difficulty_label = tk.Label(left_frame, text="Δυσκολία", anchor="w", font=("Helvetica", 13, "bold"))
        self.recipe_difficulty_label.pack(fill="x")

        self.recipe_difficulty = ttk.Combobox(left_frame, state="readonly", values=["Εύκολη", "Μέτρια", "Δύσκολη"])
        self.recipe_difficulty.bind("<<ComboboxSelected>>", lambda e: self.difficulty.set(self.recipe_difficulty.current() + 1))
        self.recipe_difficulty.pack(fill="x")


        self.recipe_time_label = tk.Label(left_frame, text="Χρόνος Προετοιμασίας", anchor="w", font=("Helvetica", 13, "bold"))
        self.recipe_time_label.pack(fill="x")


        self.recipe_time = tk.Entry(left_frame, state="readonly")
        self.recipe_time.pack(fill="x")

    # Steps

        self.add_step_button = tk.Button(main_frame, text="Προσθήκη Βήματος", command=self.add_step)
        self.add_step_button.pack()


        self.scrolled_frame = ScrolledFrame(main_frame)
        self.scrolled_frame.pack(fill="both", expand=True)
        self.steps_frame = self.scrolled_frame.display_widget(tk.Frame, fit_width=True)

        self.update_time()

        self.add_step()

    def calculate_execution_time(self):
        total_time = 0
        for step in self.steps:
            total_time += step.execution_time.get()
        self.execution_time.set(total_time)

    def get_categories(self):
        categories = list(db.RecipeCategory.select())
        return [category.name for category in categories]

    def save(self):
        # alert user that the recipe was saved
        # messagebox.showinfo("Αποθήκευση", "Η συνταγή αποθηκεώθηκε επιτυχώς", parent=self)
        recipe_data = {
            "name": self.name.get(),
            "category": self.recipe_category.get(),
            "difficulty": self.difficulty.get(),
            "execution_time": self.execution_time.get(),
            "steps": []
        }

        for step in self.steps:
            step_data = {
                "title": step.title.get(),
                "number": step.step_number.get(),
                "description": step.description.get(),
                "execution_time": step.execution_time.get(),
                "ingredients": []
            }
            for ingredient in step.ingredients_table.get_children():
                step_data["ingredients"].append(step.ingredients_table.item(ingredient)["values"][1])
            
            recipe_data["steps"].append(step_data)

        result = utilities.add_full_recipe(recipe_data)
        if result["success"]:
            self.parent.load_recipes()
            self.destroy()
            messagebox.showinfo("Αποθήκευση", "Η συνταγή αποθηκεώθηκε επιτυχώς", parent=self.parent)
        else:
            messagebox.showinfo("Αποθήκευση", f"Σφάλμα {result["message"]}", parent=self)


    def order_steps(self):
        for i, step in enumerate(self.steps):
            step.step_number.set(i + 1)

    def add_step(self):
        self.steps.append(StepFrame(self))
        # reorderging steps
        self.order_steps()


    def delete_step(self, step):
        self.steps.remove(step)
        step.destroy()
        self.calculate_execution_time()
        self.order_steps()

    def time_format(self, minutes):
        hours = minutes // 60
        minutes = minutes % 60
        return f"{hours} ώρες και {minutes} λεπτά" if hours > 0 else f"{minutes} λεπτά"
    
    def update_time(self):
        self.recipe_time.configure(state='normal')
        self.recipe_time.delete(0, tk.END)
        self.recipe_time.insert(0, self.time_format(self.execution_time.get()))
        self.recipe_time.configure(state='readonly')

    def get_ingredients(self):
        ingredients = list(db.Ingredient.select())
        # return [(ingredient.id, ingredient.name) for ingredient in ingredients]
        # return a dictionary with the id as the key and the name as the value
        return {ingredient.id: ingredient.name for ingredient in ingredients}
