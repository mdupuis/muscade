from enum import Enum
import tempfile
from app.models import Recipe


class ParserState(Enum):
    recipe_name = 0
    category = 1
    ingredients = 2
    instructions = 3

def export_to_txt(recipes):
    return_char = "\r\n"
    value = ""
    for recipe in recipes:
        value += recipe.name
        value += return_char
        value += return_char
        value += recipe.ingredients
        value += return_char
        value += return_char
        value += recipe.instructions
        value += return_char
        value += return_char
        value += return_char
    return value


def import_from_txt(web_file):
    recipes = []
    state = ParserState.recipe_name
    recipe = Recipe()
    last_line_blank = True
    for line in web_file.readlines():
        line = line.strip().decode('utf-8')
        if len(line.strip()) == 0:
            if not last_line_blank:
                state = ParserState((state.value + 1) % 3)
            last_line_blank = True
        else:
            last_line_blank = False
            if state is ParserState.recipe_name:
                if recipe.name is not None:
                    recipe.save()
                    recipes.append(recipe)
                recipe = Recipe()
                recipe.name = line.strip()
                recipe.ingredients = ""
                recipe.instructions = ""
            elif state is ParserState.category:
                recipe.category = line.strip()
            elif state is ParserState.ingredients:
                recipe.ingredients += line.strip()
            elif state is ParserState.instructions:
                recipe.instructions += line.strip()
    if state is ParserState.recipe_name and recipe.name is not None:
        recipe.save()
        recipes.append(recipe)
    return recipes