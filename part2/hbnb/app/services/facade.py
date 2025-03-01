from app.persistence.repository import InMemoryRepository
from app.models import storage
from app.models import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.storage = storage

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

    def get_amenity_by_name(self, name):
        """Retrieve an amenity by name from the repository"""
        amenities = self.amenity_repo.get_all()
        return next((a for a in amenities if a.name == name), None)

    def create_amenity(self, amenity_data):
        new_amenity = Amenity(**amenity_data)
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

    def create_place(self, place_data):
        owner_id = place_data.get("owner_id")
        
        if not owner_id:
            print("Error: No owner_id provided.")
            return None

        print(f"Owner ID being searched: {owner_id}")

        print(f"Storage: {self.storage}")

        owner = self.storage.get(User, owner_id)

        print(f"Owner found: {owner}")

        if not owner:
            print(f"Owner not found for ID: {owner_id}")
            return None

        print(f"Owner found: {owner}")

        price = place_data.get("price")
        latitude = place_data.get("latitude")
        longitude = place_data.get("longitude")

        if price is not None and (not isinstance(price, (int, float)) or price < 0):
            raise ValueError("Price must be a positive number")

        if latitude is not None and (not isinstance(latitude, (int, float)) or not -90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")

        if longitude is not None and (not isinstance(longitude, (int, float)) or not -180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")

        new_place = Place(**place_data)
        self.storage.add(new_place)
        self.storage.save()
        return new_place

    def create_place(self, place_data):
        """Create a new place with validation."""
        owner = self.storage.get(User, place_data.get("owner_id"))
        if not owner:
            raise ValueError("Owner not found")

        price = place_data.get("price")
        latitude = place_data.get("latitude")
        longitude = place_data.get("longitude")

        if price is not None and (not isinstance(price, (int, float)) or price < 0):
            raise ValueError("Price must be a positive number")

        if latitude is not None and (not isinstance(latitude, (int, float)) or not -90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")

        if longitude is not None and (not isinstance(longitude, (int, float)) or not -180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")

        new_place = Place(**place_data)
        self.storage.add(new_place)
        self.storage.save()
        return new_place

    def get_place(self, place_id):
        """Retrieve a place by ID, including owner details and amenities."""
        place = self.storage.get(Place, place_id)
        if not place:
            return None

        owner = self.storage.get(User, place.owner_id)
        owner_data = {"id": owner.id, "name": owner.name} if owner else None

        amenities = [
            {"id": amenity.id, "name": amenity.name}
            for amenity in place.amenities
        ]

        return {
            "id": place.id,
            "name": place.name,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": owner_data,
            "amenities": amenities
        }

    def get_all_places(self):
        """Retrieve all places from storage."""
        places = self.storage.all(Place)
        return [
            {
                "id": place.id,
                "name": place.name,
                "price": place.price,
                "latitude": place.latitude,
                "longitude": place.longitude,
                "owner_id": place.owner_id
            }
            for place in places
        ]

    def update_place(self, place_id, place_data):
        """Update an existing place with new data."""
        place = self.storage.get(Place, place_id)
        if not place:
            return None

        if "price" in place_data:
            price = place_data["price"]
            if not isinstance(price, (int, float)) or price < 0:
                raise ValueError("Price must be a positive number")

        if "latitude" in place_data:
            latitude = place_data["latitude"]
            if not isinstance(latitude, (int, float)) or not -90 <= latitude <= 90:
                raise ValueError("Latitude must be between -90 and 90")

        if "longitude" in place_data:
            longitude = place_data["longitude"]
            if not isinstance(longitude, (int, float)) or not -180 <= longitude <= 180:
                raise ValueError("Longitude must be between -180 and 180")

        for key, value in place_data.items():
            setattr(place, key, value)

        self.storage.save()
        return {"message": "Place updated successfully"}

    def create_review(self, review_data):
        user_id = review_data.get("user_id")
        place_id = review_data.get("place_id")
        rating = review_data.get("rating")
        text = review_data.get("text")
        
        # Validar si el usuario existe
        user = storage.get(User, user_id)
        if not user:
            print(f"User with ID {user_id} not found")  # Depuración
            raise ValueError(f"User with ID {user_id} not found")
        
        # Validar si el lugar existe
        place = storage.get(Place, place_id)
        if not place:
            print(f"Place with ID {place_id} not found")  # Depuración
            raise ValueError(f"Place with ID {place_id} not found")
        
        # Validar el rating
        if rating is None or not isinstance(rating, int) or not 1 <= rating <= 5:
            print(f"Invalid rating: {rating}")  # Depuración
            raise ValueError("Rating must be an integer between 1 and 5")
        
        # Crear la reseña
        new_review = Review(user_id=user_id, place_id=place_id, rating=rating, text=text)
        storage.add(new_review)
        storage.save()
        print(f"Review created: {new_review}")  # Depuración
        return new_review

    def get_review(self, review_id):
        review = storage.get(Review, review_id)
        if not review:
            raise ValueError(f"Review with ID {review_id} not found")
        return review

    # Método para obtener todas las reseñas
    def get_all_reviews(self):
        return storage.all(Review)

    # Método para obtener todas las reseñas de un lugar específico
    def get_reviews_by_place(self, place_id):
        place = storage.get(Place, place_id)
        if not place:
            raise ValueError(f"Place with ID {place_id} not found")
        
        return [review for review in place.reviews]

    # Método para actualizar una reseña
    def update_review(self, review_id, review_data):
        review = storage.get(Review, review_id)
        if not review:
            raise ValueError(f"Review with ID {review_id} not found")
        
        # Actualizar los campos de la reseña
        if 'text' in review_data:
            review.text = review_data.get('text')
        if 'rating' in review_data:
            new_rating = review_data.get('rating')
            if not isinstance(new_rating, int) or not 1 <= new_rating <= 5:
                raise ValueError("Rating must be an integer between 1 and 5")
            review.rating = new_rating
        
        storage.save()
        return review

    # Método para eliminar una reseña
    def delete_review(self, review_id):
        review = storage.get(Review, review_id)
        if not review:
            raise ValueError(f"Review with ID {review_id} not found")
        
        storage.delete(review)
        storage.save()
        return {"message": "Review deleted successfully"}