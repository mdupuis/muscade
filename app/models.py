from datetime import date

from peewee import fn, Model
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
    source = CharField(null=True)
    portion = IntegerField(null=True)
    preparation_time = IntegerField(null=True)
    cooking_time = IntegerField(null=True)
    rating = IntegerField(null=True)
    usage_count = IntegerField(default=0)
    add_date = DateTimeField(default=date.today())
    update_date = DateTimeField(default=date.today())

    def category_name(self):
        my_categories = [item[1] for item in categories if item[0] == self.category]
        return my_categories[0] if len(my_categories) > 0 else None

    @classmethod
    def count_per_category(cls):
        per_categories = cls.select(
            cls.category,
            fn.COUNT(cls.id).alias('count')
        ).group_by(cls.category)
        return {
            r.category: r.count for r in per_categories
        }

    @classmethod
    def count_per_source(cls, limit=None):
        per_source = cls.select(
            cls.source,
            fn.COUNT(cls.id).alias('count')
        ).where(
            ~(cls.source >> None)
        ).group_by(cls.source)

        per_source = per_source.order_by(
            fn.COUNT(cls.id).desc()
        )

        if limit:
            per_source = per_source.limit(limit)

        return per_source

    @classmethod
    def best_recipes(cls, limit=None):
        best_recipes = cls.select().order_by(
            cls.rating.desc()
        )

        if limit:
            best_recipes = best_recipes.limit(limit)

        return best_recipes


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
