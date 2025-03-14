from app.persistence.repository import InMemoryRepository
from app.models import storage
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from flask import jsonify
import uuid
from datetime import datetime
""" Facade class to interact with the storage and perform business logic """

class HBnBFacade:
    """ Facade class to interact with the storage and perform business logic """
    def __init__(self):
        """ Initialize the facade with in-memory repositories """
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.amenity_repository = InMemoryRepository()
        self.storage = storage

#------------------------------------------------------------USERS-----------------------------------------------------------------
    def get_all_users(self):
        """Retrieve all users from storage"""
        users = self.storage.all(User).values()
        return list(users)

    def create_user(self, user_data):
        """Create a new user and store in storage"""
        print(f"Received user data: {user_data}")
        new_user = User(**user_data)
        new_user.hash_password(user_data['password'])
        self.user_repo.add(new_user)
        return new_user

    def delete_user(self, user_id):
        """Delete a user by ID."""
        user = self.storage.get(User, user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        self.storage.delete(user)
        self.storage.save(user)
        return {"message": f"User {user_id} deleted successfully"}

    def get_user(self, user_id):
        """Retrieve a user by ID"""
        print(f"Fetching user with ID: {user_id}")
        return self.storage.get(User, user_id)

    def get_user_by_email(self, email):
        """Retrieve user by email"""
        return self.user_repo.get_by_attribute('email', email)
    
    def update_user(self, user_id, user_data):
        """Update an existing user with new data."""
        user = self.storage.get(User, user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        existing_user = self.get_user_by_email(user_data.get("email"))
        if existing_user and existing_user.id != user_id:
            raise ValueError("Email already registered by another user")

        for key, value in user_data.items():
            setattr(user, key, value)

        self.storage.save(user)
        return user

#------------------------------------------------------------PLACES-----------------------------------------------------------------
    def get_place(self, place_id):
        """Retrieve a place by ID and return as a dictionary"""
        place = self.storage.get(Place, place_id)
        return place.to_dict() if place else None

    def create_place(self, place_data):
        """Create a new place with validation"""
        owner = self.storage.get(User, place_data.get("owner_id"))
        if not owner:
            raise ValueError("Owner not found")

        required_fields = ["title", "price", "latitude", "longitude", "owner_id"]
        for field in required_fields:
            if field not in place_data or place_data[field] is None:
                raise ValueError(f"{field} is required")

        price = place_data["price"]
        latitude = place_data["latitude"]
        longitude = place_data["longitude"]

        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a positive number")

        if not isinstance(latitude, (int, float)) or not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90")

        if not isinstance(longitude, (int, float)) or not -180 <= longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180")

        new_place = Place(
            title=place_data.get("title"),
            description=place_data.get("description", ""),
            price=price,
            latitude=latitude,
            longitude=longitude,
            owner=owner
        )

        self.storage.save(new_place)
        return new_place.to_dict()

    def update_place(self, place_id, place_data):
        """Update an existing place"""
        place = self.storage.get(Place, place_id)
        if not place:
            return None

        for key, value in place_data.items():
            setattr(place, key, value)

        self.storage.save()
        return {"message": "Place updated successfully"}

    def get_all_places(self):
        """Retrieve all places from storage and return JSON-serializable data"""
        places = self.storage.all(Place).values()
        return [place.to_dict() for place in places]

#------------------------------------------------------------REVIEWS-----------------------------------------------------------------
    
    def create_review(self, review_data):
        """Create a new review with validation"""
        try:
            print(f"Received review data: {review_data}")

            user_id = review_data.get("user_id")
            place_id = review_data.get("place_id")
            rating = review_data.get("rating")
            text = review_data.get("text")

            print(f"Checking user with ID: {user_id}")
            user = self.storage.get(User, user_id)
            if not user:
                raise ValueError(f"User with ID {user_id} not found")

            print(f"Checking place with ID: {place_id}")
            place = self.storage.get(Place, place_id)
            if not place:
                raise ValueError(f"Place with ID {place_id} not found")

            print(f"Validating rating: {rating}")
            if rating is None or not isinstance(rating, int) or not 1 <= rating <= 5:
                raise ValueError("Rating must be an integer between 1 and 5")

            print(f"Validating review text: {text}")
            if not text or not isinstance(text, str) or text.strip() == "":
                raise ValueError("Review text cannot be empty")

            print("All validations passed. Creating review...")
            new_review = Review(
                id=str(uuid.uuid4()),
                user_id=user_id, 
                place_id=place_id, 
                rating=rating, 
                text=text,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            new_review.user = user
            new_review.place = place

            print(f"Assigned ID to review: {new_review.id}")
            self.storage.save(new_review)

            stored_review = self.storage.get(Review, new_review.id)

            print(f"Successfully created review: {stored_review}")
            return stored_review

        except Exception as e:
            print(f"Error creating review: {str(e)}")
            raise

    def get_all_reviews(self):
        """Retrieve all reviews from storage and return JSON-serializable data"""
        try:
            reviews = self.storage.all(Review).values()
            print(f"Retrieved {len(reviews)} reviews")

            # ✅ Convert each review object to dictionary
            reviews_list = [review.to_dict() for review in reviews]
            print(f"Successfully converted reviews: {reviews_list}")

            return reviews_list
        except Exception as e:
            print(f"Error retrieving reviews: {str(e)}")
            raise

    def delete_review(self, review_id):
        """Delete a review by ID"""
        review = self.storage.get(Review, review_id)
        if not review:
            raise ValueError(f"Review with ID {review_id} not found")
        
        self.storage.delete(review)
        self.storage.save()
        return {"message": "Review deleted successfully"}

#------------------------------------------------------------AMENITIES-----------------------------------------------------------------

    def create_amenity(self, amenity_data):
        """Create a new amenity and store it"""
        new_amenity = Amenity(id=str(uuid.uuid4()), name=amenity_data['name'])
        self.amenity_repository.add(new_amenity)
        return new_amenity

    def get_amenity_by_name(self, name):
        """Retrieve an amenity by name"""
        return self.amenity_repository.get_by_attribute("name", name)

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by its ID"""
        return self.amenity_repository.get(amenity_id)

    def get_all_amenities(self):
        """Retrieve all stored amenities"""
        return self.amenity_repository.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update the name of an amenity if it exists"""
        amenity = self.get_amenity(amenity_id)
        if amenity:
            amenity.name = amenity_data['name']
            self.amenity_repository.update(amenity_id, {"name": amenity.name})
            return amenity
        return None