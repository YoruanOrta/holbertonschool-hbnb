import uuid
from datetime import datetime

class BaseModel:
    def __init__(self, **kwargs):
        # Asigna un UUID por defecto si no se pasa uno
        self.id = str(uuid.uuid4()) if 'id' not in kwargs else kwargs['id']
        
        # Asigna las fechas por defecto si no se pasan
        self.created_at = datetime.now() if 'created_at' not in kwargs else kwargs['created_at']
        self.updated_at = datetime.now() if 'updated_at' not in kwargs else kwargs['updated_at']
        
        # Asigna cualquier otro parámetro que se pase a la clase
        for key, value in kwargs.items():
            setattr(self, key, value)

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp