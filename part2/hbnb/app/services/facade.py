from app.persistence.repository import InMemoryRepository
from app.models import user  # Correctly imported

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()  # Assuming you're using this repository as a mock for now
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Create user with SQLAlchemy model
    def create_user(self, user_data):
        new_user = user.User(**user_data)  # Correctly reference the 'User' class
        self.user_repo.add(new_user)  # Add the user to your in-memory repository
        return new_user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        pass