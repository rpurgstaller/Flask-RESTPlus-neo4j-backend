from flask import Flask, jsonify, request

from backend.src.entities.recipe import Recipe, RecipeSchema
from backend.src.entities.recipe_ingredient import RecipeIngredient

# creating the Flask application
app = Flask(__name__)

# Generate database later


@app.route('/recipes')
def get_recipes():
    # TODO just a dummy atm, Fetch from database later
    ingredients = [RecipeIngredient(name="sugar", ingredient_type="teaspoon", amount=2),
                   RecipeIngredient(name="rum", ingredient_type="shot", amount=1)]
    recipe_objs = [Recipe(title="test recipe", directions="Directions here",
                          ingredients=ingredients)]

    schema = RecipeSchema(many=True)
    recipes = schema.dump(recipe_objs)

    # TODO close db session
    return jsonify(recipes)


@app.route('/recipes', methods=['POST'])
def add_recipe():
    posted_recipe = RecipeSchema(only=('title', 'description')).load(request.get_json())

    recipe = Recipe(**posted_recipe.data)

    # TODO persist in database

    new_recipe = RecipeSchema().dump(recipe).data

    # TODO close session

    return jsonify(new_recipe), 201
