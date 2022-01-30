class QueryManagerNeo4j:

    def __init__(self, neo4j_connection):
        self.neo4j_connection = neo4j_connection

    @property
    def neo4j_connection(self):
        return self.__neo4jconnection

    @neo4j_connection.setter
    def neo4j_connection(self, neo4j_connection):
        self.__neo4j_connection = neo4j_connection

