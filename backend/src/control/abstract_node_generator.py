class AbstractNodeGenerator:

    def __init__(self, labels):
        self.labels = labels

    def applies(self, labels):
        return all(label in labels for label in self.__labels)

    def generate(self, labels, relationships):
        pass

    @property
    def labels(self):
        return self.__labels

    @labels.setter
    def labels(self, labels):
        self.__labels = labels

