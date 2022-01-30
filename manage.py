import os
import unittest

import click

from app import blueprint
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from enum import Enum

from app.main import create_app
from app.main.repository.db import db_connection

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(blueprint)
app.app_context().push()

manager = Manager(app)

migrate = Migrate(app)

manager.add_command('db', MigrateCommand)


class TestType(Enum):
    ALL = 'test'
    UNIT = 'test/unit'
    INTEGRATION = 'test/integration'


def _test(test_type: TestType):
    """
    Runs tests depending on the test type
    """
    tests = unittest.TestLoader().discover(test_type.value, pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@app.teardown_appcontext
def close_db(error):
    db_connection.close_db(error)


@manager.command
def run():
    app.run(host='localhost')


@manager.command
def test():
    _test(TestType.ALL)


@manager.command
def unit_tests():
    _test(TestType.UNIT)


if __name__ == '__main__':
    manager.run()
