from py2neo import NodeMatch, NodeMatcher
from py2neo.ogm import Model

from app.main.repository.base_repository import db


class MdModel(Model):

    @classmethod
    def match_by_attr(cls, k: str, v: str) -> NodeMatch:
        return cls.match(db()).where(f'_.{k}=_.{v}')

    @classmethod
    def get(cls, identity):
        return cls.wrap(NodeMatcher(db()).get(identity))
