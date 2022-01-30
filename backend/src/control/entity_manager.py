from backend.src.control.node_generator import EntityGenerator
from backend.src.control.recipe_generator import RecipeGenerator


class EntityManager:

    def __init__(self):
        self.__generators = [RecipeGenerator(),
                             EntityGenerator()]

    def _get_entity_generators(self, labels):
        result_set = [ng for ng in self.__generators if ng.applies(labels)]

        assert len(result_set) > 0, "No node generator found for node labels: " + labels

        return result_set

    def create(self, labels, relationships):

        node_generators = self._get_entity_generators(labels)

        nodes = []

        for ng in node_generators:
            nodes.append(ng.generate(labels, relationships))

        return nodes



