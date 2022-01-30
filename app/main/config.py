import os

from app.main.logging_config import Handler, init

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # todo generate secrete key
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False
    NEO4J_URL = os.getenv('NEO4J_URL')
    NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
    NEO4J_PW = os.getenv('NEO4J_PW')
    LOG_DIR = f'{os.getenv("HOME")}/logs/project_medusa'
    LOG_HANDLERS = [Handler.STDOUT, Handler.FILE]

    @classmethod
    def init_logging(cls) -> None:
        init(log_dir=cls.LOG_DIR, handlers=cls.LOG_HANDLERS)


class DevelopmentConfig(Config):
    DEBUG = True
    LOG_HANDLERS = [Handler.STDOUT, Handler.FILE]


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    LOG_HANDLERS = [Handler.STDOUT]


class ProductionConfig(Config):
    DEBUG = False
    LOG_HANDLERS = [Handler.FILE]


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
