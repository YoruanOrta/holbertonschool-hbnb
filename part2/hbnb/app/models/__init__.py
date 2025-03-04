import uuid
from app.models.user import User

class MemoryStorage:
    """Almacenamiento temporal en memoria"""
    
    def __init__(self):
        self.data = {}

    def get(self, model, obj_id):
        """Obtiene un objeto por ID"""
        print(f"🔍 Retrieving {model.__name__} with ID: {obj_id}")
        return self.data.get(obj_id)

    def save(self, obj):
        """Guarda un objeto en memoria"""
        if not hasattr(obj, 'id') or obj.id is None:
            obj.id = str(uuid.uuid4())
        
        print(f"Saving {obj.__class__.__name__} with ID: {obj.id}")
        self.data[obj.id] = obj

    def delete(self, obj):
        """Elimina un objeto por su ID"""
        if obj.id in self.data:
            print(f"🗑️ Deleting {obj.__class__.__name__} with ID: {obj.id}")
            del self.data[obj.id]

    def all(self, model=None):
        """Retorna todos los objetos almacenados, filtrados por modelo opcionalmente"""
        if model:
            return {obj_id: obj for obj_id, obj in self.data.items() if isinstance(obj, model)}
        return self.data

storage = MemoryStorage()