import uuid
from app.models.user import User
from app.persistence import InMemoryRepository
""" Models module """

class MemoryStorage(InMemoryRepository):
    """Temporary in-memory storage"""

    def __init__(self):
        self.data = {}

    def get(self, model, obj_id):
        """Gets an object by ID"""
        print(f"🔍 Retrieving {model.__name__} with ID: {obj_id}")
        return self.data.get(obj_id)

    def save(self, obj):
        """Saves an object in memory"""
        if not hasattr(obj, 'id') or obj.id is None:
            obj.id = str(uuid.uuid4())
        
        print(f"Saving {obj.__class__.__name__} with ID: {obj.id}")
        self.data[obj.id] = obj

    def delete(self, obj):
        """Deletes an object by its ID"""
        if obj.id in self.data:
            print(f"🗑️ Deleting {obj.__class__.__name__} with ID: {obj.id}")
            del self.data[obj.id]

    def all(self, model=None):
        """Returns all stored objects, optionally filtered by model"""
        if model:
            return {obj_id: obj for obj_id, obj in self.data.items() if isinstance(obj, model)}
        return self.data

storage = MemoryStorage()