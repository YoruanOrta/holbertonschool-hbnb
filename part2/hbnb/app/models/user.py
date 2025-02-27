from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class User(BaseModel):
    email = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    is_admin = Column(Boolean, nullable=False, default=False)
    places = relationship('Place', backref='user', cascade='all, delete')
    reviews = relationship('Review', backref='user', cascade='all, delete')

    def __init__(self, email, first_name=None, last_name=None, is_admin=False):
        super().__init__()
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin