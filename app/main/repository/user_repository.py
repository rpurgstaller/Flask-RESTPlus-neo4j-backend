import datetime

from py2neo import NodeMatcher
from py2neo.ogm import Repository

from app.main.repository.db.db_connection import db
from app.main.model.user import User
from app.main.repository.db.db_util import get_as_regexp_case_insensitive
from app.main.repository.base_repository import BaseRepository

USER_NODE_NAME = 'u'
USER_ID_NAME = 'user_id'


class UserRepository(BaseRepository):

    def __init__(self):
        super().__init__(model=User)

    def delete_marked(self):
        self.delete(self.match().where(f'_:{User.LABEL_NAME_DELETED}'))
