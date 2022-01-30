class Neo4jQuery:

    def __init__(self, stmt):
        self.stmt = stmt
        self.params = {}

    def invoke(self, neo4j_connection):
        response = neo4j_connection.query(self.stmt, self.params)
        return response

    @property
    def stmt(self):
        return self.__stmt

    @stmt.setter
    def stmt(self, stmt):
        self.__stmt = stmt

    @property
    def params(self):
        return self.__params

    @params.setter
    def params(self, params):
        self.__params = params

    def add_param(self, name, value):
        self.__params[name] = value
