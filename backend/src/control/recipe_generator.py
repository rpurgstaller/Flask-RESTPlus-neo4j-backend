from backend.src.control.abstract_node_generator import AbstractNodeGenerator
from backend.src.entities.recipe import Recipe


class RecipeGenerator(AbstractNodeGenerator):

    def __init__(self):
        AbstractNodeGenerator.__init__(self, ["recipe"])

    def generate(self, labels, relationships):
        return Recipe(labels, relationships)

