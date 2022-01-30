from neo4j import GraphDatabase, basic_auth

from app.main.repository.db.db_connection import IDatabaseConnection


class Neo4jConnection(IDatabaseConnection):

    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None

    def initialize(self):
        try:
            self.__driver = GraphDatabase.driver(self.__uri,
                                                 auth=basic_auth(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create neo4j driver:", e)

    def assert_driver_init(self):
        assert self.__driver is not None, "neo4j driver is not initialized"

    def close(self):
        self.assert_driver_init()
        self.__driver.close()

    def query(self, stmt, params):
        self.assert_driver_init()

        session, response = None, None

        try:
            session = self.__driver.session()
            response = list(session.run(stmt, params=params))
        except Exception as e:
            print("Failed to execute query " + stmt + ". Exception: " + e)
        finally:
            if session is not None:
                session.close()

        return response


