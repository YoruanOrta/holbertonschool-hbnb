from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api import create_api
""" Create a Flask app and configure it with the API """

def create_app(testing=False):
    """ Create a Flask app and configure it with the API """
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    if testing:
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    api.add_namespace(users_ns, path='/api/v1/users')
    create_api(app)
    return app