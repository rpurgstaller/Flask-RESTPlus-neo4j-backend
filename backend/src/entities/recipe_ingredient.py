class RecipeIngredient:

    def __init__(self, name, ingredient_type, amount):
        self.name = name
        self.ingredient_type = ingredient_type
        self.amount = amount

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def ingredient_type(self):
        return self._ingredient_type

    @ingredient_type.setter
    def ingredient_type(self, ingredient_type):
        self._ingredient_type = ingredient_type

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, amount):
        self._amount = amount


