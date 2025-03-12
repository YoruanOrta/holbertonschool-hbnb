from flask import Flask
from flask_restx import Api
from app.api import create_api
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def create_app(config_class=None):
    """Create a Flask application and configure it with the API"""
    app = Flask(__name__)

    # Use the provided configuration or a default one
    if config_class:
        app.config.from_object(config_class)

    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    # Register the API namespaces
    from app.api.v1.users import api as users_ns
    api.add_namespace(users_ns, path='/api/v1/users')

    # Register other endpoints or API configurations
    create_api(app)

    bcrypt.init_app(app)

    return app