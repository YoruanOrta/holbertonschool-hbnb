import re
from sqlalchemy import Column, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship, validates
from app.models.base_model import BaseModel
from app.models.user import User
from app.models.review import Review
from app.models.amenity import Amenity
""" Place Module for the HBNB project """


class Place(BaseModel):
    """ A place to stay """
    title = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    owner_id = Column(String(60), ForeignKey('users.id'), nullable=False)

    owner = relationship("User", back_populates="places")
    reviews = relationship("Review", back_populates="place", cascade="all, delete", lazy="select")
    amenities = relationship("Amenity", secondary="place_amenity", back_populates="places", lazy="select")

    def __init__(self, title, description, price, latitude, longitude, owner):
        """ Constructor for Place class """
        super().__init__()
        self.title = self.validate_title("title", title)
        self.description = description if description else "No description"
        self.price = self.validate_price("price", price)
        self.latitude = self.validate_latitude("latitude", latitude)
        self.longitude = self.validate_longitude("longitude", longitude)
        self.owner = owner

    def to_dict(self):
        """Convert Place object to a dictionary"""
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "price": float(self.price),
            "latitude": float(self.latitude),
            "longitude": float(self.longitude),
            "owner_id": str(self.owner.id) if self.owner else None, 
            "owner": {
                "id": str(self.owner.id),
                "first_name": self.owner.first_name,
                "last_name": self.owner.last_name,
                "email": self.owner.email
            } if self.owner else None,
            "reviews": [
                review.to_dict() for review in self.reviews or []
            ] if isinstance(self.reviews, list) else [],
            "amenities": [
                amenity.to_dict() for amenity in self.amenities or []
            ] if isinstance(self.amenities, list) else [],
        }


    @validates('title')
    def validate_title(self, key, value):
        """Validate that the title is not empty"""
        if not value or not isinstance(value, str) or value.strip() == "":
            raise ValueError("Title cannot be empty and must be a string")
        return value

    @validates('price')
    def validate_price(self, key, value):
        """Validate that the price is a positive number"""
        if value is None or not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Price must be a positive number")
        return value

    @validates('latitude')
    def validate_latitude(self, key, value):
        """Validate that the latitude is between -90 and 90"""
        if value is None or not isinstance(value, (int, float)) or not -90 <= value <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        return value

    @validates('longitude')
    def validate_longitude(self, key, value):
        """Validate that the longitude is between -180 and 180"""
        if value is None or not isinstance(value, (int, float)) or not -180 <= value <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        return value