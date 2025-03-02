import re
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship, validates
from app.models.base_model import BaseModel

class User(BaseModel):
    email = Column(String(128), nullable=False, unique=True)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    is_admin = Column(Boolean, nullable=False, default=False)
    places = relationship('Place', backref='user', cascade='all, delete')
    reviews = relationship('Review', backref='user', cascade='all, delete')

    def __init__(self, email, first_name=None, last_name=None, is_admin=False):
        super().__init__()
        if not self.validate_email(email):
            raise ValueError("Invalid email format")
        self.email = email
        self.first_name = self.validate_names("first_name", first_name)
        self.last_name = self.validate_names("last_name", last_name)
        self.is_admin = is_admin

        if not self.validate_email(email):
            raise ValueError("Invalid email format")
        self.email = email

    @staticmethod
    def validate_email(email):
        """Valida que el email tenga un formato correcto"""
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(email_regex, email) is not None

    @validates('first_name', 'last_name')
    def validate_names(self, key, value):
        """Valida que first_name y last_name no sean cadenas vacías"""
        if value and value.strip() == "":
            raise ValueError(f"{key} cannot be empty")
        return value