from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from flask_bcrypt import Bcrypt
from app.extensions import db, bcrypt
from flask_jwt_extended import JWTManager
from config import DevelopmentConfig

from app.api.v1.auth import api as auth_ns
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns

bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class=DevelopmentConfig):
    """Create a Flask application and configure it with the API"""

    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config.from_object(config_class)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hbnb.db'  
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app