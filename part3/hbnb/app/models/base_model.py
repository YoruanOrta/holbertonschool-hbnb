from app.extensions import db
import uuid
from datetime import datetime

"""Base class for all models in the application"""

class BaseModel(db.Model):
    __abstract__ = True 

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        """Initialize a new model instance with optional attributes"""
        super().__init__(**kwargs)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def save(self):
        """Update the updated_at timestamp and commit the session"""
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """Update object attributes based on provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()