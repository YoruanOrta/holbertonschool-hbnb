from app.persistence.repository import InMemoryRepository
from app.models import User
from app.models.amenity import Amenity  # Importa la clase Amenity correctamente

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Crear usuario
    def create_user(self, user_data):
        new_user = User(**user_data)
        self.user_repo.add(new_user)
        return new_user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_place(self, place_id):
        pass

    # Buscar amenity por nombre
    def get_amenity_by_name(self, name):
        """Retrieve an amenity by name from the repository"""
        amenities = self.amenity_repo.get_all()
        return next((a for a in amenities if a.name == name), None)

    # Crear amenity
    def create_amenity(self, amenity_data):
        new_amenity = Amenity(**amenity_data)  # Crear el amenity correctamente
        self.amenity_repo.add(new_amenity)
        return new_amenity

        self.create_amenity({"name": "Wi-Fi"})
        self.create_amenity({"name": "Air Conditioning"})

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None

        for key, value in amenity_data.items():
            setattr(amenity, key, value)

        self.amenity_repo.update(amenity_id, amenity)
        return amenity