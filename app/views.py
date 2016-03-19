# coding=utf-8

from flask import render_template, request, flash, redirect, url_for, abort
from flask import make_response

from . import app
from .export import export_to_txt, import_from_txt
from .models import categories, Recipe, RecipeForm


@app.context_processor
def inject_categories():
    return dict(categories=categories)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
def home():
    count_by_categories = Recipe.count_per_category()

    source_recipes = Recipe.count_per_source(limit=5)

    best_recipes = Recipe.best_recipes(limit=5)

    return render_template("home.html",
                           title='Accueil',
                           categories_values=count_by_categories,
                           source_recipes=source_recipes,
                           best_recipes=best_recipes)


@app.route('/list')
def list():
    recipes = Recipe.select()
    return render_template("list.html",
                           title='Liste',
                           show_source=True,
                           show_category=True,
                           ids=" ".join([str(recipe.id) for recipe in recipes]),
                           recipes=recipes)


@app.route('/category/<int:category_id>')
def by_category(category_id):
    recipes = Recipe.select().where(Recipe.category == category_id)
    category_names = [x[1] for x in categories if x[0] == category_id]

    return render_template("list.html",
                           title='Catégories',
                           header_suffix=category_names[0] if len(category_names) else None,
                           show_source=True,
                           ids=" ".join([str(recipe.id) for recipe in recipes]),
                           recipes=recipes)


@app.route('/source/<name>')
def by_source(name):
    recipes = Recipe.select().where(Recipe.source == name)

    return render_template("list.html",
                           title='Catégories',
                           header_suffix=name,
                           ids=" ".join([str(recipe.id) for recipe in recipes]),
                           show_category=True,
                           recipes=recipes)


@app.route('/search')
def search():
    query = request.args.get('s')
    recipes = Recipe.select().where(Recipe.name ** ('%%%s%%' % query) |
                                    Recipe.ingredients ** ('%%%s%%' % query) |
                                    Recipe.instructions ** ('%%%s%%' % query))
    if (recipes.count() == 1):
        return render_template("view_recipe_page.html",
                               recipe=recipes[0])
    else:
        return render_template("list.html",
                               title='Recherche',
                               header_suffix=query,
                               ids=" ".join([str(recipe.id) for recipe in recipes]),
                               recipes=recipes)


@app.route('/<int:recipe_id>/', methods=['GET', 'POST'])
def view_recipe(recipe_id):
    recipe = None
    try:
        recipe = Recipe.select().where(Recipe.id == recipe_id).get()
    except Recipe.DoesNotExist:
        abort(404)
    return render_template("view_recipe_page.html",
                           recipe=recipe)


@app.route('/<int:recipe_id>/fs', methods=['GET', 'POST'])
def view_recipe_fs(recipe_id):
    recipe = None
    try:
        recipe = Recipe.select().where(Recipe.id == recipe_id).get()
    except Recipe.DoesNotExist:
        abort(404)
    return render_template("view_recipe_fs.html",
                           recipe=recipe)


@app.route('/multiple/<ids>', methods=['GET', 'POST'])
def view_multiple(ids):
    id_list = ids.split()
    recipes = Recipe.select().where(Recipe.id << id_list)
    response = render_template("base_nav.html")
    for recipe in recipes:
        response += render_template("view_recipe.html", recipe=recipe, multiple=True)
    return response


@app.route('/export/<ids>', methods=['GET', 'POST'])
def export(ids):
    id_list = ids.split()
    recipes = Recipe.select().where(Recipe.id << id_list)
    response = make_response(export_to_txt(recipes))
    response.headers['Content-Type'] = 'text/plain'
    response.headers['Content-Disposition'] = 'attachment; filename=export.txt'
    return response


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']

        if file:
            recipes = import_from_txt(file)
            return render_template("list.html",
                                   title="Résultat de l'importation",
                                   ids=" ".join([str(recipe.id) for recipe in recipes]),
                                   recipes=recipes)
    else:
        return render_template("base_nav.html") + """<br/><br/><br/><br/>
            <form action="/upload" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
"""


@app.route('/<int:recipe_id>/edit/', methods=['GET', 'POST'])
@app.route('/add/', methods=['GET', 'POST'])
def edit_recipe(recipe_id=None):
    entry = None
    if recipe_id:
        # edit
        try:
            entry = Recipe.get(id=recipe_id)
        except Recipe.DoesNotExist:
            abort(404)
    else:
        # add
        entry = Recipe()
    if request.method == 'POST':
        # submit
        form = RecipeForm(request.form, obj=entry)
        if form.validate():
            form.populate_obj(entry)
            entry.save()
            flash('Modifications sauvegardées', 'success')
            return redirect(url_for('view_recipe', recipe_id=entry.id))
    else:
        # print the form
        form = RecipeForm(obj=entry)

    return render_template('edit.html', form=form, entry=entry)
