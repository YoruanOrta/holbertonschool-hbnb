from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
""" API module for reviews """


api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

facade = HBnBFacade()

@api.route('/')
class ReviewList(Resource):
    """ Shows a list of all reviews, and lets you POST to add new reviews """
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        try:
            review_data = api.payload
            review = facade.create_review(review_data)
            
            print(f"Successfully created review: {review}")
            
            review_dict = review.to_dict()
            print(f"Review dict: {review_dict}")
            
            return review_dict, 201

        except ValueError as e:
            print(f"ValueError: {str(e)}")
            return {'error': str(e)}, 400
        except Exception as e:
            print(f"Exception: {str(e)}")
            return {'error': 'An error occurred while creating the review'}, 500


    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        try:
            reviews = facade.get_all_reviews()
            if not reviews:
                return {"message": "No reviews found"}, 200
            return reviews, 200
        except Exception as e:
            print(f"Exception in GET /reviews/: {str(e)}")
            return {'error': 'An error occurred while retrieving reviews'}, 500

@api.route('/<review_id>')
class ReviewResource(Resource):
    """ Show a single review item and lets you update or delete them """
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        try:
            review = facade.get_review(review_id)
            return review.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 404
        except Exception as e:
            return {'error': 'An error occurred while retrieving the review'}, 500

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        try:
            review_data = api.payload
            updated_review = facade.update_review(review_id, review_data)
            return updated_review.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 404
        except Exception as e:
            return {'error': 'An error occurred while updating the review'}, 500

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        try:
            response = facade.delete_review(review_id)
            return response, 200
        except ValueError as e:
            return {'error': str(e)}, 404
        except Exception as e:
            return {'error': 'An error occurred while deleting the review'}, 500

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    """ Show a list of all reviews for a specific place """
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return [review.to_dict() for review in reviews], 200
        except ValueError as e:
            return {'error': str(e)}, 404
        except Exception as e:
            return {'error': 'An error occurred while retrieving reviews for the place'}, 500