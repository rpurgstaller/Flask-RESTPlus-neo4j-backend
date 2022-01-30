from __future__ import annotations
from flask import g
from py2neo import Graph, NodeMatcher
from py2neo.ogm import Repository

from app.main.config import Config


def db():
    if not hasattr(g, 'neo4j_db'):
        g.neo4j_db = Graph(Config.NEO4J_URL, auth=(Config.NEO4J_USERNAME, Config.NEO4J_PW))
    return g.neo4j_db


class BaseRepository(Repository):

    def __init__(self, model):
        self._model = model

    @classmethod
    def wrap(cls, graph):
        obj = cls()
        obj.graph = graph
        return obj

    @classmethod
    def get(cls) -> BaseRepository:
        return cls.wrap(db())

    def match(self, primary_value=None):
        return super().match(self._model, primary_value)

    def node_match(self, *labels, **properties):
        if self._model is not None:
            if self._model.__primarylabel__ is not None:
                t = [*labels, self._model.__primarylabel__]
                return NodeMatcher(db()).match(*t, **properties)

        return NodeMatcher(db()).match(*labels, **properties)
