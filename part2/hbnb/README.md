# HBNB Project - Business Logic Layer

## Table of Contents

- [HBNB Project - Business Logic Layer](#hbnb-project---business-logic-layer)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Project Structure](#project-structure)
  - [Business Logic Layer](#business-logic-layer)
    - [Entities](#entities)
    - [Classes and Methods](#classes-and-methods)
    - [Place Example](#place-example)
    - [Review Example](#review-example)
    - [Amenity Example](#amenity-example)
  - [Responsibilities of the Business Logic Layer](#responsibilities-of-the-business-logic-layer)
  - [Workflow](#workflow)

---

## Introduction

The **HBNB** project is a system for managing users, places, reviews, and amenities in an accommodation service.  
This document describes the **Business Logic Layer (BLL)**, which handles data processing, entity management, and interactions between the API and the database.

---

## Project Structure

The project follows a **layered architecture**:

1. **Presentation Layer** – The API (Flask) that handles HTTP requests.
2. **Business Logic Layer (BLL)** – Processes data and enforces business rules.
3. **Persistence Layer** – Uses SQLAlchemy for database management.

The **Business Logic Layer** acts as an intermediary, ensuring that all operations comply with business rules.

---

## Business Logic Layer

### Entities

The main entities in the system are:

| Entity   | Description |
|----------|------------|
| **User** | Manages user accounts, authentication, and interactions. |
| **Place** | Represents accommodations like apartments, houses, and hotels. |
| **Review** | Stores user-generated reviews for places. |
| **Amenity** | Represents features available in places (e.g., WiFi, Pool). |

---

### Classes and Methods

```python
from models import User, Place, Review, Amenity

# ------------------ User Class ------------------
class User:
    def __init__(self, email, first_name, last_name):
        self.id = None
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
    
    def save(self):
        """Saves the user to the database."""
        pass

    def update(self, **kwargs):
        """Updates user information."""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def delete(self):
        """Removes the user."""
        pass

    def to_dict(self):
        """Returns a dictionary representation of the user."""
        return self.__dict__

# ------------------ Place Class ------------------
class Place:
    def __init__(self, name, description, user_id):
        self.id = None
        self.name = name
        self.description = description
        self.city = city
        self.user_id = user_id

    def save(self):
        """Saves the place."""
        pass

    def update(self, **kwargs):
        """Updates the place."""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def delete(self):
        """Removes the place."""
        pass

    def to_dict(self):
        """Returns a dictionary representation of the place."""
        return self.__dict__

# ------------------ Review Class ------------------
class Review:
    def __init__(self, text, rating, place_id, user_id):
        self.id = None
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    def save(self):
        """Saves the review."""
        pass

    def delete(self):
        """Removes the review."""
        pass

    def to_dict(self):
        """Returns a dictionary representation of the review."""
        return self.__dict__

# ------------------ Amenity Class ------------------
class Amenity:
    def __init__(self, name):
        self.id = None
        self.name = name

    def save(self):
        """Saves the amenity."""
        pass

    def delete(self):
        """Removes the amenity."""
        pass

    def to_dict(self):
        """Returns a dictionary representation of the amenity."""
        return self.__dict__

# ------------------ Usage Examples ------------------

## Usage Examples

### User Example

```python
user = User(email="john.doe@example.com", first_name="John", last_name="Doe")
user.save()
user.update(first_name="Jonathan")
print(user.to_dict())
user.delete()
```

### Place Example

```python
place = Place(name="Beach House", description="A beautiful house by the sea", user_id=1)
place.save()
place.update(description="Now with a pool!")
print(place.to_dict())
place.delete()
```

### Review Example

```python
review = Review(text="Amazing place!", rating=5, place_id=1, user_id=2)
review.save()
print(review.to_dict())
review.delete()
```

### Amenity Example

```python
amenity = Amenity(name="WiFi")
amenity.save()
print(amenity.to_dict())
amenity.delete()
```

## Responsibilities of the Business Logic Layer

 • Data Validation: Ensures input data is valid before saving to the database.
 • Business Rules Enforcement: Guarantees that operations follow the required rules (e.g., only authenticated users can create places).
 • Data Transformation: Converts database models into JSON responses for the API.
 • Inter-layer Communication: Bridges the persistence layer and API, ensuring smooth data flow.

## Workflow

 1. A user registers via the API.
 2. The business logic layer validates and processes the request.
 3. The persistence layer saves the user to the database.
 4. When creating a place, the system verifies the user’s existence.
 5. Reviews are linked to both users and places.
 6. Amenities can be associated with places.

    AUTHOR:
  Yoruan Orta Bonilla
