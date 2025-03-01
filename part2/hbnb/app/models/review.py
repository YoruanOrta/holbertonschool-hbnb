from app.models.base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class Review(BaseModel):
    __tablename__ = 'reviews'
    
    text = Column(String(1024), nullable=False)
    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    place = relationship('Place', backref='reviews')
    user = relationship('User', backref='reviews')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)