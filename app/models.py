from datetime import date

from peewee import Model
from peewee import (CharField, DateTimeField, IntegerField, PrimaryKeyField,
                    TextField)
from wtfpeewee.orm import model_form

from app import db

categories = [(0, "Entrées"), (1, "Repas principaux"), (2, "Desserts"), (3, "Accompagnements"), (4, "Autres")]


class BaseModel(Model):
    class Meta:
        database = db


class Recipe(BaseModel):
    id = PrimaryKeyField()
    name = CharField()
    category = IntegerField()
    ingredients = TextField()
    instructions = TextField()
    source = CharField()
    portion = IntegerField()
    preparation_time = IntegerField()
    cooking_time = IntegerField()
    rating = IntegerField()
    usage_count = IntegerField(default=0)
    add_date = DateTimeField(default=date.today())
    update_date = DateTimeField(default=date.today())

    def category_name(self):
        my_categories = [item[1] for item in categories if item[0] == self.category]
        return my_categories[0] if len(my_categories) > 0 else None


RecipeForm = model_form(Recipe,
                        exclude=['add_date', 'update_date', 'usage_count'],
                        field_args={
                            "name": {"label": "Nom"},
                            "ingredients": {"label": "Ingrédients"},
                            "preparation_time": {"label": "Temps de préparation"},
                            "cooking_time": {"label": "Temps de cuisson"},
                            "category": {"choices": categories,
                                         "label": "Catégorie"},
                            "rating": {"validators": [],
                                       "label": "Note"}})


# db.create_tables([Recipe])
