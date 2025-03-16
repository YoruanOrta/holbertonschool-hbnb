from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy  # ✅ Import SQLAlchemy
from config import DevelopmentConfig

from app.api.v1.auth import api as auth_ns
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns

bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()  # ✅ Initialize SQLAlchemy

def create_app(config_class=DevelopmentConfig):
    """Create a Flask application and configure it with the API"""

    app = Flask(__name__)
    app.config.from_object(config_class)

    # ✅ Add database URI (Make sure it's set in your config)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hbnb.db'  
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # ✅ Recommended

    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    # ✅ Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # ✅ Create database tables
    with app.app_context():
        db.create_all()

    # Register the API namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app