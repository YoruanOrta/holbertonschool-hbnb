from app.models.base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, validates
from datetime import datetime

class Review(BaseModel):
    __tablename__ = 'reviews'
    
    text = Column(String(1024), nullable=False)
    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    place = relationship('Place', back_populates='reviews')
    user = relationship('User', back_populates='reviews')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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