from app.models.user import User

class MemoryStorage:
    """Almacenamiento temporal en memoria (ejemplo)"""
    def __init__(self):
        self.data = {}

    def get(self, model, obj_id):
        """Obtiene un objeto por ID"""
        return self.data.get(obj_id)

    def save(self, obj):
        """Guarda un objeto"""
        self.data[obj.id] = obj

storage = MemoryStorage()  # Instancia de almacenamiento