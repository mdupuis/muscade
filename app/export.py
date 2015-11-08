
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