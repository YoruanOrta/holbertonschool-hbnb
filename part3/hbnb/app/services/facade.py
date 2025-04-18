from app.persistence.repository import SQLAlchemyRepository
from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.review_repository import ReviewRepository
from app.persistence.amenity_repository import AmenityRepository
from app.models import storage
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
import uuid
from datetime import datetime
""" Facade class to interact with the storage and perform business logic """

class HBnBFacade:
    """ Facade class to interact with the storage and perform business logic """
    def __init__(self):
        """ Initialize the facade with in-memory repositories """
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)
        self.amenity_repository = SQLAlchemyRepository(Amenity)
        self.storage = storage

#------------------------------------------------------------USERS-----------------------------------------------------------------
    def get_all_users(self):
        """Retrieve all users from storage"""
        users = self.storage.all(User).values()
        return list(users)

    def create_user(self, user_data):
        """Create a new user and store in storage"""
        print(f"Received user data: {user_data}")
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

    def delete_user(self, user_id):
        """Delete a user by ID."""
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        self.user_repo.delete(user_id)
        return {"message": f"User {user_id} deleted successfully"}

    def get_user(self, user_id):
        """Retrieve a user by ID"""
        print(f"Fetching user with ID: {user_id}")
        return self.user_repo.get(User, user_id)

    def get_user_by_email(self, email):
        """Retrieve user by email"""
        return self.user_repo.get_by_attribute('email', email)
    
    def update_user(self, user_id, user_data):
        """Update an existing user with new data."""
        user = self.user_repo.get(User, user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        existing_user = self.get_user_by_email(user_data.get("email"))
        if existing_user and existing_user.id != user_id:
            raise ValueError("Email already registered by another user")

        for key, value in user_data.items():
            setattr(user, key, value)

        self.user_repo.add(user)
        return user

#------------------------------------------------------------PLACES-----------------------------------------------------------------
    def get_place(self, place_id):
        """Retrieve a place by ID and return as a dictionary"""
        place = self.place_repo.get(place_id)
        return place.to_dict() if place else None

    def create_place(self, place_data):
        """Create a new place with validation"""
        owner_id = place_data.get("owner_id")

        owner = self.user_repo.get(owner_id) 

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
            owner_id=owner_id
        )

        self.place_repo.add(new_place)
        return new_place.to_dict()

    def update_place(self, place_id, data):
        """Update an existing place"""
        place = self.place_repo.get(place_id)
        if not place:
            return None

        for key, value in data.items():
            if hasattr(place, key):
                setattr(place, key, value)

        self.place_repo.update(place_id, data)
        return {"message": "Place updated successfully"}

    def get_all_places(self):
        """Retrieve all places from storage and return JSON-serializable data"""
        return [place.to_dict() for place in self.place_repo.get_all()]

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
            user = self.user_repo.get(user_id)
            if not user:
                raise ValueError(f"User with ID {user_id} not found")

            print(f"Checking place with ID: {place_id}")
            place = self.place_repo.get(place_id)
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

            print(f"Assigned ID to review: {new_review.id}")
            self.review_repo.add(new_review)

            stored_review = self.review_repo.get(new_review.id)
            print(f"Successfully created review: {stored_review}")
            return stored_review.to_dict()

        except Exception as e:
            print(f"Error creating review: {str(e)}")
            raise

    def get_review(self, review_id):
        """Fetch a review by its ID."""
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError(f"Review with ID {review_id} not found.")
        return review

    def save_review(self, review):
        """Save a review to repository"""
        try:
            print(f"Saving review: {review.id}")
            self.review_repo.add(review)
        except Exception as e:
            print(f"Error saving review: {str(e)}")
            raise

    def get_all_reviews(self):
        """Retrieve all reviews and return JSON-serializable data"""
        try:
            reviews = self.review_repo.get_all()
            print(f"Retrieved {len(reviews)} reviews")

            reviews_list = [review.to_dict() for review in reviews]
            print(f"Successfully converted reviews: {reviews_list}")

            return reviews_list
        except Exception as e:
            print(f"Error retrieving reviews: {str(e)}")
            raise

    def update_review(self, review_id, review_data):
        """Update the review with new data."""
        review = self.get_review(review_id)
        if not review:
            raise ValueError(f"Review with ID {review_id} not found.")

        review.text = review_data.get("text", review.text)
        review.rating = review_data.get("rating", review.rating)
        review.updated_at = datetime.utcnow()

        self.save_review(review)

        return review.to_dict()

#------------------------------------------------------------AMENITIES-----------------------------------------------------------------

    def create_amenity(self, amenity_data):
        """Create a new amenity and store it"""
        try:
            print(f"Creating amenity with data: {amenity_data}")
            new_amenity = Amenity(
                id=str(uuid.uuid4()),
                name=amenity_data["name"],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            self.amenity_repo.add(new_amenity)
            stored_amenity = self.amenity_repo.get(new_amenity.id)
            print(f"Amenity created successfully: {stored_amenity}")
            return stored_amenity
        except Exception as e:
            print(f"Error creating amenity: {str(e)}")
            raise


    def get_amenity_by_name(self, name):
        """Retrieve an amenity by name"""
        return self.amenity_repo.get_by_attribute("name", name)


    def get_amenity(self, amenity_id):
        """Retrieve an amenity by its ID"""
        return self.amenity_repo.get(amenity_id)


    def get_all_amenities(self):
        """Retrieve all stored amenities"""
        return self.amenity_repo.get_all()


    def update_amenity(self, amenity_id, amenity_data):
        """Update the name of an amenity if it exists"""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError(f"Amenity with ID {amenity_id} not found")

        print(f"Updating amenity {amenity_id} with data: {amenity_data}")
        amenity.name = amenity_data["name"]
        amenity.updated_at = datetime.utcnow()
        self.amenity_repo.update(amenity_id, {"name": amenity.name, "updated_at": amenity.updated_at})

        updated_amenity = self.amenity_repo.get(amenity_id)
        return updated_amenity