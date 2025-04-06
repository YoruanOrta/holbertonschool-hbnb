from app.models.base_model import BaseModel
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from app.extensions import db
""" Amenity Module for the HBNB project """

class Amenity(BaseModel, db.Model):
    """ Amenity class to store information about an Amenity """
    __tablename__ = 'amenities'
    name = db.Column(db.String(128), nullable=False, unique=True)
    places = relationship("Place", secondary="place_amenities", back_populates="amenities", lazy="select")

    def __repr__(self):
        return f"<Amenity {self.name}>"