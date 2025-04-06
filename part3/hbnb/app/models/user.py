import re
from app.extensions import db, bcrypt
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import relationship, validates
from app.models.base_model import BaseModel
""" User module """

bcrypt = Bcrypt()

class User(BaseModel, db.Model):
    """ User class """
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = relationship('Place', backref='user', cascade='all, delete-orphan')
    reviews = relationship('Review', backref='user', cascade='all, delete-orphan')

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