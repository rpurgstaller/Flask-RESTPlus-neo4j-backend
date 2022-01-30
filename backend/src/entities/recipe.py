from marshmallow import Schema, fields


class Recipe:

    def __init__(self, title, directions, ingredients):
        self.title = title
        self.directions = directions
        self.ingredients = ingredients

    @property
    def title(self):
        return self._name

    @title.setter
    def title(self, name):
        self._name = name

    @property
    def directions(self):
        return self._name

    @directions.setter
    def directions(self, directions):
        self._directions = directions

    @property
    def ingredients(self):
        return self._ingredients

    @ingredients.setter
    def ingredients(self, ingredients):
        self._ingredients = ingredients

    def get_ingredient_names(self, lower=False):
        if lower:
            return [ingredient.title.lower() for ingredient in self._ingredients]

        return [ingredient.title for ingredient in self._ingredients]

    def has_ingredients(self, ingredient_names):
        return all(name in self.get_ingredient_names(True) for name in ingredient_names)


class RecipeSchema(Schema):
    title = fields.Str()
    directions = fields.Str()


