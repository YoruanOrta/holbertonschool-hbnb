from flask_restx import Namespace, Resource, fields
from flask import request , jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade
from app.services.review_service import ReviewService

""" API module for reviews """

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user (Auto-filled from JWT)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

facade = HBnBFacade()
review_service = ReviewService(facade.storage)

@api.route('/')
class ReviewList(Resource):
    """ Shows a list of all reviews, and lets you POST to add new reviews """

    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'You cannot review your own place')
    @api.response(409, 'You have already reviewed this place')
    @jwt_required()
    def post(self):
        """Register a new review (Authenticated Users Only)"""
        current_user = get_jwt_identity()
        review_data = request.get_json()
        review_data["user_id"] = current_user  # Ensure user_id is set to the logged-in user

        place = facade.get_place(review_data["place_id"])
        if not place:
            return {'error': 'Place not found'}, 404

        # Prevent users from reviewing their own place
        if place["owner_id"] == current_user:
            return {'error': 'You cannot review your own place'}, 403

        try:
            new_review = facade.create_review(review_data)
            return new_review, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews (Public Access)"""
        try:
            reviews = facade.get_all_reviews()
            if not reviews:
                return {"message": "No reviews found"}, 200
            return reviews, 200
        except Exception as e:
            return {'error': 'An error occurred while retrieving reviews'}, 500

@api.route('/<review_id>')
class ReviewResource(Resource):
    """ Show a single review item and lets you update or delete it """

    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID (Public Access)"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, review_id):
        """Update a review (Only the author can modify)"""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            return {'error': 'Review not found'}, 404
        if review.user_id != current_user:
            return {'error': 'Unauthorized action'}, 403

        review_data = request.get_json()
        try:
            updated_review = facade.update_review(review_id, review_data)
            return updated_review, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(204, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review by ID"""

        # Get the current user's ID from the JWT token
        current_user_id = get_jwt_identity()

        try:
            # Fetch the review using the ReviewService
            review = review_service.get_review(review_id)

            # Check if the review exists
            if not review:
                return jsonify({"message": f"Review with ID {review_id} not found"}), 404

            # Check if the current user is the owner of the review
            if review.user_id != current_user_id:
                return jsonify({"message": "You are not authorized to delete this review"}), 403

            # Proceed with deleting the review using ReviewService
            review_service.delete_review(review_id, current_user_id)

            # ✅ Return an empty response with 204 No Content (no jsonify)
            return '', 204

        except ValueError as e:
            return jsonify({"message": str(e)}), 400

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    """ Show a list of all reviews for a specific place """

    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place (Public Access)"""
        try:
            reviews = facade.get_reviews_by_place(place_id)
            if not reviews:
                return {"message": "No reviews found for this place"}, 200
            return reviews, 200
        except ValueError as e:
            return {'error': str(e)}, 404
        except Exception as e:
            return {'error': 'An error occurred while retrieving reviews'}, 500