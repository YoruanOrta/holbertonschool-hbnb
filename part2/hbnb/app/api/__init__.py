from flask_restx import Api
from flask import Blueprint
from app.api.v1.users import api as users_api
from app.api.v1.amenities import api as amenities_api

# Crear Blueprint para la API
api_bp = Blueprint("api", __name__, url_prefix="/api/v1")

# Crear la instancia de Api una sola vez
api = Api(api_bp, version="1.0", title="HBnB API", description="API for the HBnB application", doc="/docs")

# Registrar namespaces
api.add_namespace(users_api, path="/users")
api.add_namespace(amenities_api, path="/amenities")

def create_api(app):
    """ Registra el Blueprint en la aplicación """
    app.register_blueprint(api_bp)