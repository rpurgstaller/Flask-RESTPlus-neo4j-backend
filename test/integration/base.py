from flask_testing import TestCase
from manage import app


class BaseIntegrationTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object('app.main.config.TestingConfig')
        return app

    def setUp(self):
        pass

    def tearDown(self):
        pass
