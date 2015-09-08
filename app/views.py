from flask import render_template, request, flash, redirect, url_for, abort
from app import app
from .models import *


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
@app.route('/index')
def index():
    recipes = Recipe.select()
    return render_template("list.html",
                           title='Home',
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
