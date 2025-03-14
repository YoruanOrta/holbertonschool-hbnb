from flask_restx import Api
from flask import Blueprint
from app.api.v1.users import api as users_api
from app.api.v1.amenities import api as amenities_api
from app.api.v1.places import api as places_api
from app.api.v1.reviews import api as reviews_api
from app.api.v1.auth import api as auth_api


api_bp = Blueprint("api", __name__, url_prefix="/api/v1")

api = Api(api_bp, version="1.0", title="HBnB API", description="API for the HBnB application", doc="/docs")

api.add_namespace(users_api, path="/users")
api.add_namespace(amenities_api, path="/amenities")
api.add_namespace(places_api, path="/places")
api.add_namespace(reviews_api, path="/reviews")
api.add_namespace(auth_api, path="/auth")

def create_api(app):
    """ Registra el Blueprint en la aplicación """
    app.register_blueprint(api_bp)