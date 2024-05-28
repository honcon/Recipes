from peewee import *
from playhouse.pool import PooledSqliteDatabase

db = PooledSqliteDatabase("recipes.db", max_connections=2, stale_timeout=300)


class BaseModel(Model):
    class Meta:
        database = db


class RecipeCategory(BaseModel):
    id = AutoField()
    name = CharField(unique=True)

    class Meta:
        db_table = "recipe_category"


class Recipe(BaseModel):
    id = AutoField()
    name = CharField(unique=True)
    category = ForeignKeyField(RecipeCategory, backref="recipes")
    difficulty = IntegerField()
    execution_time = IntegerField()


class Ingredient(BaseModel):
    id = AutoField()
    name = CharField()


class Step(BaseModel):
    id = AutoField()
    recipe_id = ForeignKeyField(Recipe, backref="steps")
    title = CharField()
    description = TextField()
    number = IntegerField()
    execution_time = IntegerField()


class RecipesIngredients(BaseModel):
    recipe_id = ForeignKeyField(Recipe, backref="recipes_ingredients_details")
    ingredient_id = ForeignKeyField(Ingredient, backref="used_in_recipes")
    step_id = ForeignKeyField(Step, backref="ingredient_steps")

    class Meta:
        db_table = "recipes_ingredients"


def init_db():
    db.connect()
    db.execute_sql('PRAGMA foreign_keys = ON;')
    db.create_tables([RecipeCategory, Recipe, Ingredient, Step, RecipesIngredients])
