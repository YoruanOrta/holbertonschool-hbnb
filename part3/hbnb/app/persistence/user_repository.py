from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    """Repository for user-specific data operations"""

    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        """Fetch a user by email"""
        return self.model.query.filter_by(email=email).first()

    def email_exists(self, email):
        """Check if a user already exists with this email"""
        return self.get_user_by_email(email) is not None

    def authenticate(self, email, password):
        """Verify email and password combination"""
        user = self.get_user_by_email(email)
        if user and user.verify_password(password):
            return user
        return None