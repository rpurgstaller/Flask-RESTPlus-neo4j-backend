from flask import g
from py2neo import Graph
from neo4j import GraphDatabase, basic_auth

from app.main.config import Config


def close_db(error):
    pass

    #if hasattr(g, 'neo4j_db'):
    #    g.neo4j_db


def db():
    if not hasattr(g, 'neo4j_db'):
        g.neo4j_db = Graph(Config.NEO4J_URL, auth=(Config.NEO4J_USERNAME, Config.NEO4J_PW))
        #g.neo4j_db = GraphDatabase.driver(Config.NEO4J_URL,
        #                                  auth=basic_auth(Config.NEO4J_USERNAME, str(Config.NEO4J_PW))).session()
    return g.neo4j_db

