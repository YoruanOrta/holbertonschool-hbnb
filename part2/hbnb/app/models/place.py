from app.models.base_model import BaseModel
from app.models.user import User

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        if not isinstance(title, str):
            raise TypeError("title must be a string")
        if not isinstance(description, str):
            raise TypeError("description must be a string")
        if not isinstance(price, (int, float)):
            raise TypeError("price must be a number")
        if not isinstance(latitude, (int, float)):
            raise TypeError("latitude must be a number")
        if not isinstance(longitude, (int, float)):
            raise TypeError("longitude must be a number")
        if not isinstance(owner, User):
            raise TypeError("owner must be a User object")
        
        self.title = title if title else "Untitled"
        self.description = description if description else "No description"
        self.price = price if price >= 0 else 0.0
        self.latitude = latitude if -90 <= latitude <= 90 else 0.0
        self.longitude = longitude if -180 <= longitude <= 180 else 0.0
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)