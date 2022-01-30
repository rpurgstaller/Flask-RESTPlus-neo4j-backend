from flask_restplus import Namespace, fields


class RecipeDto:
    NAMESPACE_NAME = 'recipe'

    api = Namespace(NAMESPACE_NAME, 'a recipe of some kind')

    recipe = api.model(NAMESPACE_NAME, {
        'title': fields.String(required=True, description='Title of the recipe'),
        'directions': fields.String(required=True, description="Directions for the recipe")
    })
