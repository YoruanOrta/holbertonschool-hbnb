from app.models.review import Review

class ReviewService:
    """Handles business logic for managing reviews."""
    
    def __init__(self, storage):
        self.storage = storage

    def add_review(self, review):
        """Adds a review to storage."""
        if isinstance(review, Review):
            self.storage.save(review)
        else:
            raise ValueError("Only Review objects can be added.")
    
    def get_review(self, review_id):
        """Fetch a review by its ID."""
        return self.storage.get(Review, review_id)

    def update_review(self, review_id, review_data):
        """Update a review."""
        review = self.get_review(review_id)
        if review:
            review.text = review_data.get("text", review.text)
            review.rating = review_data.get("rating", review.rating)
            self.storage.save(review)
            return review
        else:
            raise ValueError("Review not found.")

    def delete_review(self, review_id, user_id):
        """Delete a review."""
        review = self.get_review(review_id)
        if review:
            # Check if the user is authorized to delete the review
            if review.user_id != user_id:
                raise ValueError("You are not authorized to delete this review.")
            # Delete the review from storage
            self.storage.delete(review)
        else:
            raise ValueError("Review not found.")