from app.extensions import db
from app.models.base_model import BaseModel
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, validates
from sqlalchemy import Integer
""" Review Module for the HBNB project """

class Review(BaseModel, db.Model):
    """ Review class to store review information """
    __tablename__ = 'reviews'

    text = db.Column(String(1024), nullable=False)
    rating = db.Column(Integer, nullable=False)
    place_id = db.Column(String(60), ForeignKey('places.id'), nullable=False)
    user_id = db.Column(String(60), ForeignKey('users.id'), nullable=False)
    place = relationship("Place", back_populates="reviews")

    def to_dict(self):
        """Convert Review object to a dictionary without nested objects"""

        if not hasattr(self, "id") or not self.id:
            print("Error: Review ID is missing!")
            raise ValueError("Review object is missing an ID")

        try:
            print(f"Checking attributes:")
            print(f"   - Text: {self.text}")
            print(f"   - Rating: {self.rating}")
            print(f"   - Place ID: {self.place_id}")
            print(f"   - User ID: {self.user_id}")
            print(f"   - Created At: {self.created_at}")
            print(f"   - Updated At: {self.updated_at}")

            review_dict = {
                "id": str(self.id),
                "text": self.text,
                "rating": self.rating,
                "place_id": self.place_id,
                "user_id": self.user_id,
                "created_at": self.created_at.isoformat(),
                "updated_at": self.updated_at.isoformat(),
            }

            print(f"Successfully converted to dict: {review_dict}")
            return review_dict

        except Exception as e:
            print(f"Exception inside to_dict(): {str(e)}")
            raise

    @validates('text')
    def validate_text(self, key, value):
        """Validate that the review text is not empty"""
        if not value or not isinstance(value, str) or value.strip() == "":
            raise ValueError("Review text cannot be empty")
        return value

    @validates('user_id')
    def validate_user_id(self, key, value):
        """Validate that the user_id is a valid string"""
        if not value or not isinstance(value, str):
            raise ValueError("User ID must be a valid string")
        return value

    @validates('place_id')
    def validate_place_id(self, key, value):
        """Validate that the place_id is a valid string"""
        if not value or not isinstance(value, str):
            raise ValueError("Place ID must be a valid string")
        return value
    
    def __repr__(self):
        return f"<Review {self.id} - Rating: {self.rating}>"
