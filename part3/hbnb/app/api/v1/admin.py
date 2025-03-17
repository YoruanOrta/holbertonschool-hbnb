from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
""" API endpoints for admin operations """


api = Namespace('admin', description='Admin operations')

""" Models """
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner': fields.Nested(api.model('Owner', {
        'id': fields.String(description='User ID of the owner'),
        'first_name': fields.String(description='First name of the owner'),
        'last_name': fields.String(description='Last name of the owner'),
        'email': fields.String(description='Email of the owner')
    })),
    'amenities': fields.List(fields.String, description="List of amenity IDs"),
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})


@api.route('/users/')
class AdminUserCreate(Resource):
    """Resource for creating and retrieving users"""
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload
        email = user_data.get('email')

        # Check if email is already in use
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        user_data["is_admin"] = True

        try:
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email
            }, 201
        except (ValueError, TypeError, AssertionError) as e:
            return {"error": str(e)}, 400
        

    @api.response(200, 'List of users retrieved successfully')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def get(self):
        """Get all users (only admins can perform this action)"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        users = facade.user_repo.get_all()
        return [
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
            for user in users
        ], 200


@api.route('/users/<user_id>')
class AdminUserModify(Resource):
    @jwt_required()
    def put(self, user_id):
        """Update user details"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        data = request.json
        email = data.get('email')

        # Ensure email uniqueness
        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        updated_details = api.payload
        updated_user = facade.update_user(user_id, updated_details)
        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200


@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new amenity"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        amenity_data = api.payload
        new_amenity = facade.create_amenity(amenity_data)
        return {
            'id': new_amenity.id,
            'name': new_amenity.name
        }, 201
    

@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity's information"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        updated_details = api.payload
        facade.update_amenity(amenity_id, updated_details)
        return {"message": "Amenity updated successfully"}, 200


@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, place_id):
        """Update place details"""
        current_user = get_jwt_identity()

        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = facade.get_place(place_id)
        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        if not place:
            return {"error": "Place not found"}, 404
        
        updated_details = api.payload
        updated_amenities = []
        for amenity_id in updated_details.get('amenities', []):
            amenity = facade.get_amenity(amenity_id)
            if amenity:
                updated_amenities.append(amenity)

        updated_details['amenities'] = updated_amenities

        if 'owner_id' in updated_details:
            updated_owner = facade.get_user(updated_details['owner_id'])
            if updated_owner:
                updated_details["owner_id"] = updated_owner
            else:
                return {"error": "Owner not found"}, 404
            
        facade.update_place(place_id, updated_details)
        return {"message": "Place updated successfully"}, 200
    

    @api.response(200, "Place deleted successfully")
    @api.response(404, "Place not found")
    @jwt_required()
    def delete(self, place_id):
        """Delete a review"""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')
        place = facade.get_place(place_id)
        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403
        if not place:
            return {"error": "Place not found"}, 404
        facade.delete_place(place_id)
        return {"message": "Place deleted successfully"}


@api.route('/reviews/<review_id>')
class AdminReviewModify(Resource):
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """Update a review"""
        current_user = get_jwt_identity()

        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        review = facade.get_review(review_id)
        if not is_admin and review.user_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        if not review:
            return {"error": "Review not found"}, 404
        
        updated_details = api.payload
        updated_data = {}
        
        if "text" in updated_details:
            updated_data["text"] = updated_details["text"]

        if "rating" in updated_details:
            if not isinstance(updated_details["rating"], int) or not (1 <= updated_details["rating"] <= 5):
                return {"error": "Rating must be an integer between 1 and 5"}, 400
            updated_data["rating"] = updated_details["rating"]
            
        facade.update_review(review_id, updated_data)
        return {"message": "Review updated successfully"}, 200
    

    @api.response(200, "Review deleted successfully")
    @api.response(404, "Review not found")
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')
        review = facade.get_review(review_id)
        if not is_admin and review.user_id != user_id:
            return {'error': 'Unauthorized action'}, 403
        if not review:
            return {"error": "Review not found"}, 404
        facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}
