import uuid
from app.models.base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, validates
from datetime import datetime
from sqlalchemy import Integer

class Review(BaseModel):
    __tablename__ = 'reviews'
    
    id = Column(String(60), primary_key=True)
    text = Column(String(1024), nullable=False)
    rating = Column(Integer, nullable=False)
    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    reviews = relationship("Review", back_populates="place", cascade="all, delete", lazy="joined")
    place = relationship('Place', back_populates='reviews')
    user = relationship('User', back_populates='reviews')

    def __init__(self, **kwargs):
        """Ensure ID is generated correctly"""
        super().__init__(**kwargs)
        if not hasattr(self, "id") or not self.id:
            self.id = str(uuid.uuid4())


    import uuid
from app.models.base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey, DateTime, Integer
from sqlalchemy.orm import relationship, validates
from datetime import datetime

class Review(BaseModel):
    __tablename__ = 'reviews'
    
    id = Column(String(60), primary_key=True)
    text = Column(String(1024), nullable=False)
    rating = Column(Integer, nullable=False)
    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    place = relationship('Place', back_populates='reviews')
    user = relationship('User', back_populates='reviews')

    def __init__(self, **kwargs):
        """Ensure ID is generated correctly"""
        super().__init__(**kwargs)

        if not hasattr(self, "id") or not self.id:
            self.id = str(uuid.uuid4())

        print(f"Assigned ID to review: {self.id}")

    def to_dict(self):
        """Convert Review object to a dictionary with debugging"""
        print(f"Debugging to_dict() - Review ID: {self.id}")

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

            print("Checking user relationship...")
            user_dict = None
            if self.user is not None:
                try:
                    user_dict = {
                        "id": str(self.user.id) if hasattr(self.user, "id") else None,
                        "first_name": getattr(self.user, "first_name", None),
                        "last_name": getattr(self.user, "last_name", None),
                        "email": getattr(self.user, "email", None)
                    }
                except Exception as e:
                    print(f"Error fetching user details: {str(e)}")

            print("Checking place relationship...")
            place_dict = None
            if self.place is not None:
                try:
                    place_dict = {
                        "id": str(self.place.id) if hasattr(self.place, "id") else None
                    }
                except Exception as e:
                    print(f"Error fetching place details: {str(e)}")

            print(f"User data: {user_dict}")
            print(f"Place data: {place_dict}")

            review_dict = {
                "id": str(self.id),
                "text": self.text,
                "rating": self.rating,
                "place_id": self.place_id,
                "user_id": self.user_id,
                "created_at": self.created_at.isoformat(),
                "updated_at": self.updated_at.isoformat(),
                "user": user_dict,
                "place": place_dict
            }

            print(f"Successfully converted to dict: {review_dict}")
            return review_dict

        except Exception as e:
            print(f"Exception inside to_dict(): {str(e)}")
            raise




    @validates('text')
    def validate_text(self, key, value):
        """Valida que el texto de la reseña no esté vacío"""
        if not value or not isinstance(value, str) or value.strip() == "":
            raise ValueError("Review text cannot be empty")
        return value

    @validates('user_id')
    def validate_user_id(self, key, value):
        """Valida que el user_id sea un string válido"""
        if not value or not isinstance(value, str):
            raise ValueError("User ID must be a valid string")
        return value

    @validates('place_id')
    def validate_place_id(self, key, value):
        """Valida que el place_id sea un string válido"""
        if not value or not isinstance(value, str):
            raise ValueError("Place ID must be a valid string")
        return value