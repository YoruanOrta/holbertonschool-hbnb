import re
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship, validates
from app.models.base_model import BaseModel
import bcrypt
from flask_bcrypt import Bcrypt
""" User module """

bcrypt = Bcrypt()

class User(BaseModel):
    """ User class """
    __tablename__ = 'users'

    email = Column(String(128), nullable=False, unique=True)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    places = relationship('Place', backref='user', cascade='all, delete')
    reviews = relationship('Review', backref='user', cascade='all, delete')
    password = Column(String(256), nullable=False)
    is_admin = Column(Boolean, default=False)

    def __init__(self, email, password, first_name=None, last_name=None, is_admin=False):
        """ Constructor """
        super().__init__()
        if not self.validate_email(email):
            raise ValueError("Invalid email format")
        self.email = email
        self.first_name = self.validate_names("first_name", first_name)
        self.last_name = self.validate_names("last_name", last_name)
        self.is_admin = is_admin

        if password:
            self.hash_password(password)

    @staticmethod
    def validate_email(email):
        """Validate that the email has a correct format"""
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(email_regex, email) is not None

    @validates('first_name', 'last_name')
    def validate_names(self, key, value):
        """Validate that first_name and last_name are not empty strings"""
        if value and value.strip() == "":
            raise ValueError(f"{key} cannot be empty")
        return value
    
    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)