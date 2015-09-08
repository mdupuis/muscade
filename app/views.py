# coding=utf-8
from flask import render_template, request, flash, redirect, url_for, abort
from app import app
from .models import *

@app.context_processor
def inject_categories():
    return dict(categories=categories)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
@app.route('/index')
def index():
    recipes = Recipe.select()
    return render_template("list.html",
                           title='Accueil',
                           recipes=recipes)


@app.route('/category/<int:category_id>')
def by_category(category_id):
    recipes = Recipe.select().where(Recipe.category == category_id)
    category_names = [x[1] for x in categories if x[0] == category_id]

    return render_template("list.html",
                           title='Catégories',
                           header_suffix=category_names[0] if len(category_names) else None,
                           recipes=recipes)

@app.route('/search')
def search():
    query = request.args.get('s')
    recipes = Recipe.select().where(Recipe.name ** ('%%%s%%' % query) |
                                    Recipe.ingredients ** ('%%%s%%' % query) |
                                    Recipe.instructions ** ('%%%s%%' % query))
    return render_template("list.html",
                           title='Recherche',
                           header_suffix=query,
                           recipes=recipes)


@app.route('/<int:recipe_id>/', methods=['GET', 'POST'])
def view_recipe(recipe_id):
    recipe = None
    try:
        recipe = Recipe.select().where(Recipe.id == recipe_id).get()
    except Recipe.DoesNotExist:
        abort(404)
    return render_template("view_recipe.html",
                           recipe=recipe,
    )


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
