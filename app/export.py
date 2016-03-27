from enum import Enum

from app.models import Recipe


class ParserState(Enum):
    recipe_name = 0
    recipe_info = 1
    ingredients = 2
    instructions = 3

def export_to_txt(recipes):
    return_char = "\r\n"
    value = ""
    for recipe in recipes:
        value += recipe.name
        value += return_char
        value += str(recipe.category)
        value += "\t"
        value += recipe.source
        value += "\t"
        value += str(recipe.rating)
        value += "\t"
        value += str(recipe.preparation_time)
        value += "\t"
        value += str(recipe.cooking_time)
        value += "\t"
        value += str(recipe.portion)
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
    return_char = "\r\n"
    recipes = []
    state = ParserState.recipe_name
    recipe = Recipe()
    last_line_blank = True
    for line in web_file.readlines():
        line = line.strip().decode('utf-8')
        if len(line.strip()) == 0:
            if not last_line_blank:
                state = ParserState((state.value + 1) % (len(ParserState)))
            last_line_blank = True
        else:
            last_line_blank = False
            if state is ParserState.recipe_name:
                if recipe.name is not None:
                    recipe.ingredients = recipe.ingredients.strip()
                    recipe.instructions = recipe.instructions.strip()
                    recipe.save()
                    recipes.append(recipe)
                recipe = Recipe()
                recipe.name = line.strip()
                recipe.ingredients = ""
                recipe.instructions = ""
                state = ParserState.recipe_info
            elif state is ParserState.recipe_info:
                values = line.strip().split("\t")
                recipe.category = int(values[0])
                recipe.source = values[1]
                recipe.rating = int(values[2])
                recipe.preparation_time = int(values[3])
                recipe.cooking_time = int(values[4])
                recipe.portion = int(values[5])
            elif state is ParserState.ingredients:
                recipe.ingredients += line.strip() + return_char
            elif state is ParserState.instructions:
                recipe.instructions += line.strip() + return_char
    if state is ParserState.recipe_name and recipe.name is not None:
        recipe.ingredients = recipe.ingredients.strip()
        recipe.instructions = recipe.instructions.strip()
        recipe.save()
        recipes.append(recipe)
    return recipes