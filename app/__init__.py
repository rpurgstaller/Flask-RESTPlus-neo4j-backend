# app/__init__.py

from flask_restplus import Api
from flask import Blueprint

from app.main.controller.auth_controller import api as auth_ns
from app.main.controller.user_controller import api as user_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTPLUS API BOILER-PLATE',
          version='1.0',
          description='a boilerplate for flask restplus web service'
          )

api.add_namespace(auth_ns)
api.add_namespace(user_ns, path='/users')
