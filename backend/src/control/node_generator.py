from backend.src.control.abstract_node_generator import AbstractNodeGenerator


class EntityGenerator(AbstractNodeGenerator):

    def __init__(self):
        AbstractNodeGenerator.__init__(self, ["node"])

    def generate(self, labels, relationships):
        return Node(labels, relationships)

