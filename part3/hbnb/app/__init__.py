from flask import Flask
from flask_restx import Api
from app.api import create_api
from app import config
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class=config.DevelopmentConfig):
    """Create a Flask application and configure it with the API"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    # Register the API namespaces
    from app.api.v1.users import api as users_ns
    api.add_namespace(users_ns, path='/api/v1/users')

    # Register other endpoints or API configurations
    create_api(app)

    bcrypt.init_app(app)
    jwt.init_app(app)

    return app