from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade

""" API module for places """

api = Namespace('places', description='Place operations')
facade = HBnBFacade()

amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

place_model = api.model('Place', {
    "title": fields.String(required=True, description="Title of the place"),
    "description": fields.String(description="Description of the place"),
    "price": fields.Float(required=True, description="Price per night"),
    "latitude": fields.Float(required=True, description="Latitude of the place"),
    "longitude": fields.Float(required=True, description="Longitude of the place"),
    "owner_id": fields.String(required=True, description="ID of the owner"),
    "owner": fields.Nested(user_model, description="Owner of the place"),
    "amenities": fields.List(fields.String, required=True, description="List of amenities ID's"),
    "reviews": fields.List(fields.Nested(review_model), description="List of reviews")
})

@api.route('/')
class PlaceList(Resource):
    """Shows a list of all places and lets you POST to add new places"""
    
    def get(self):
        """Retrieve a list of all places (Public Access)"""
        places = facade.get_all_places()
        return places, 200

    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new place (Authenticated Users Only)"""
        current_user = get_jwt_identity()
        print(f"JWT Identity Retrieved: {current_user}")

        place_data = request.get_json()

        place_data["owner_id"] = current_user if isinstance(current_user, str) else current_user["id"]

        print(f"Place Data: {place_data}")

        try:
            new_place = facade.create_place(place_data)
            return new_place, 201
        except ValueError as e:
            return {"error": str(e)}, 400

@api.route('/<place_id>')
class PlaceResource(Resource):
    """Show a single place item and lets you update it"""

    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID (Public Access)"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return place, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information (Only Owner)"""
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404
        if place["owner_id"] != current_user:
            return {"error": "Unauthorized action"}, 403

        place_data = request.get_json()
        try:
            updated_place = facade.update_place(place_id, place_data)
            return updated_place, 200 
        except ValueError as e:
            return {"error": str(e)}, 400

    @api.response(204, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def delete(self, place_id):
        """Delete a place (Only Owner)"""
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404
        if place["owner_id"] != current_user["id"]:
            return {"error": "Unauthorized action"}, 403

        facade.delete_place(place_id)
        return {}, 204