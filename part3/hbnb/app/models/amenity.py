from app.models.base_model import BaseModel
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
""" Amenity Module for the HBNB project """

class Amenity(BaseModel):
    """ Amenity class to store information about an Amenity """
    name = Column(String(128), nullable=False)
    place_amenities = relationship('Place', secondary='place_amenity', back_populates="amenities", lazy="joined")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    def __init__(self, name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name if name else "Unknown"
        self.place_amenities = []
        self.reviews = []
        self.amenities = []