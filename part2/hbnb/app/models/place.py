import re
from sqlalchemy import Column, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship, validates
from app.models.base_model import BaseModel
from app.models.user import User

class Place(BaseModel):
    title = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    owner_id = Column(String(60), ForeignKey('users.id'), nullable=False)

    owner = relationship("User", back_populates="places")
    reviews = relationship("Review", back_populates="place", cascade="all, delete")
    amenities = relationship("Amenity", secondary="place_amenity", back_populates="places")

    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = self.validate_title("title", title)
        self.description = description if description else "No description"
        self.price = self.validate_price("price", price)
        self.latitude = self.validate_latitude("latitude", latitude)
        self.longitude = self.validate_longitude("longitude", longitude)
        self.owner = owner

    @validates('title')
    def validate_title(self, key, value):
        """Valida que el título no esté vacío"""
        if not value or not isinstance(value, str) or value.strip() == "":
            raise ValueError("Title cannot be empty and must be a string")
        return value

    @validates('price')
    def validate_price(self, key, value):
        """Valida que el precio sea un número positivo"""
        if value is None or not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Price must be a positive number")
        return value

    @validates('latitude')
    def validate_latitude(self, key, value):
        """Valida que la latitud esté entre -90 y 90"""
        if value is None or not isinstance(value, (int, float)) or not -90 <= value <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        return value

    @validates('longitude')
    def validate_longitude(self, key, value):
        """Valida que la longitud esté entre -180 y 180"""
        if value is None or not isinstance(value, (int, float)) or not -180 <= value <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        return value