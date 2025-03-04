# HBNB Project - Business Logic Layer

This project is part of the HBNB system, which manages users, places, reviews, and amenities for an accommodation service. Below is a description of the business logic layer, which contains the main entities of the system, their responsibilities, and usage examples.

## Business Logic Layer

The business logic layer is responsible for managing business rules, interactions between entities, and communication with the database. This layer acts as an intermediary between the presentation layer (API) and the persistence layer (database), ensuring that operations on data follow business rules.

### Entities

The main entities managed in this project are:

1. **User**
   - **Responsibility**: Represents a user in the system, with personal information and their role (e.g., regular user, admin).
   - **Attributes**:
     - `id`: Unique identifier for the user.
     - `email`: The user's email address.
     - `first_name`: The user's first name.
     - `last_name`: The user's last name.
   - **Relationships**: Can have multiple `Place` and `Review`.

2. **Place**
   - **Responsibility**: Represents a place where users can stay, such as a hotel, apartment, etc.
   - **Attributes**:
     - `id`: Unique identifier for the place.
     - `name`: The name of the place.
     - `description`: Description of the place.
     - `user_id`: The ID of the user who created the place.
   - **Relationships**: Can have multiple `Review` and may be associated with multiple `Amenity`.

3. **Review**
   - **Responsibility**: Represents a review left by a user for a place.
   - **Attributes**:
     - `id`: Unique identifier for the review.
     - `text`: The review text.
     - `rating`: Rating for the place (e.g., 1 to 5).
     - `place_id`: The ID of the place being reviewed.
     - `user_id`: The ID of the user who wrote the review.
   - **Relationships**: Each review is associated with a `User` and a `Place`.

4. **Amenity**
   - **Responsibility**: Represents an amenity available at a place (e.g., "WiFi", "Air conditioning", etc.).
   - **Attributes**:
     - `id`: Unique identifier for the amenity.
     - `name`: Name of the amenity.
   - **Relationships**: Can be associated with multiple `Place`.

### Classes and Methods

1. User Class
   - **Description**: The `User` class manages a user's personal information and their interactions with places and reviews.
   - **Methods**:
     - `__init__(self, email, password, first_name, last_name)`: Initializes a new user with basic information.
     - `to_dict(self)`: Converts the `User` object into a dictionary for easy JSON manipulation.
     - `save(self)`: Saves the user to the database.
     - `update(self, **kwargs)`: Updates the user's information.
     - `delete(self)`: Deletes the user from the database.

   **Usage Example**:

   ```python
   from models import User

   # Create a new user
   user = User(email="john.doe@example.com", password="password123", first_name="John", last_name="Doe")
   user.save()  # Saves the user to the database

   # Update user information
   user.update(first_name="Jonathan")

   # Get user data in dictionary format
   user_dict = user.to_dict()
   print(user_dict)  # {'id': 1, 'email': 'john.doe@example.com', 'first_name': 'Jonathan'}

   # Delete the user
   user.delete()

2. Place Class
	•	Description: The Place class manages information about a place where users can stay.
	•	Methods:
	•	__init__(self, name, description, city, user_id): Initializes a new place with basic information.
	•	to_dict(self): Converts the Place object into a dictionary for easy JSON manipulation.
	•	save(self): Saves the place to the database.
	•	update(self, **kwargs): Updates the place’s information.
	•	delete(self): Deletes the place from the database.

Usage Example:

from models import Place

# Create a new place
place = Place(name="Beach House", description="A beautiful house by the sea", city="Malibu", user_id=1)
place.save()  # Saves the place to the database

# Update place information
place.update(description="A beautiful house with a pool by the sea")

# Get place data in dictionary format
place_dict = place.to_dict()
print(place_dict)  # {'id': 1, 'name': 'Beach House', 'city': 'Malibu', 'description': 'A beautiful house with a pool by the sea'}

# Delete the place
place.delete()

3. Review Class
	•	Description: The Review class manages reviews left by users for places.
	•	Methods:
	•	__init__(self, text, rating, place_id, user_id): Initializes a new review.
	•	to_dict(self): Converts the Review object into a dictionary.
	•	save(self): Saves the review to the database.
	•	delete(self): Deletes the review from the database.

Usage Example:

from models import Review

# Create a new review
review = Review(text="Great place to stay!", rating=5, place_id=1, user_id=1)
review.save()  # Saves the review to the database

# Get review data in dictionary format
review_dict = review.to_dict()
print(review_dict)  # {'id': 1, 'text': 'Great place to stay!', 'rating': 5}

# Delete the review
review.delete()

4. Amenity Class
	•	Description: The Amenity class represents amenities available at places.
	•	Methods:
	•	__init__(self, name): Initializes a new amenity.
	•	to_dict(self): Converts the Amenity object into a dictionary.
	•	save(self): Saves the amenity to the database.
	•	delete(self): Deletes the amenity from the database.

Usage Example:

from models import Amenity

# Create a new amenity
amenity = Amenity(name="WiFi")
amenity.save()  # Saves the amenity to the database

# Get amenity data in dictionary format
amenity_dict = amenity.to_dict()
print(amenity_dict)  # {'id': 1, 'name': 'WiFi'}

# Delete the amenity
amenity.delete()

Responsibilities of the Business Logic Layer
	•	Entity Management: The business logic layer manages entities like User, Place, Review, and Amenity, ensuring that all business rules are followed when interacting with them.
	•	Database Interaction: The classes in this layer interact with the database through methods that save, update, retrieve, and delete entities.
	•	Business Logic Abstraction: The business logic layer encapsulates the logic behind system operations. For example, creating a Place ensures all values are valid before saving them to the database.
	•	Facilitating Communication with the Presentation Layer: It provides high-level methods that allow the presentation layer (API) to easily interact with the data without worrying about the complexity of database operations.

Workflow:

1.	
The API controller (presentation layer) receives a request.

2.	
It calls the facade to perform the requested operation (create, retrieve, update, or delete an entity).

3.	
The facade calls the corresponding methods of the entity classes to perform the database operations.

4.	
The response is sent back to the presentation layer (API) to be returned to the client.