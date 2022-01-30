from app.main.repository.db.db_connection import db
from app.main.model.blacklist_token import BlacklistToken
from app.main.repository.base_repository import BaseRepository


class BlacklistRepository(BaseRepository):

    def __init__(self):
        super().__init__(BlacklistToken)

