# HBnB Project

## Overview

HBnB is a scalable web application built using Flask, following a layered architecture with clear separation of concerns: API (presentation), services (business logic), and persistence (data access). The goal is to build a modular, testable, and production-ready backend system, starting with an in-memory repository and transitioning to a database using SQLAlchemy.

---

## Project Structure

```
hbnb/
├── app/
│   ├── __init__.py               # Initialize Flask app
│   ├── api/                      # REST API endpoints
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/                   # Business entities
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/                 # Facade and logic layer
│   │   ├── __init__.py
│   │   └── facade.py
│   ├── persistence/              # Repositories (in-memory/SQLAlchemy)
│   │   ├── __init__.py
│   │   └── repository.py
├── run.py                        # Application entry point
├── config.py                     # Environment configs
├── requirements.txt              # Project dependencies
├── README.md
```

---

## Setup Instructions

### Clone the project

```bash
git clone <your-repo-url>
cd hbnb
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the App

Start the Flask app with:

```bash
python run.py
```

You can test the API at `http://localhost:5000/api/v1/`.

---

## Configuration

`config.py`:

```python
import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
```

Environment selection is handled in `run.py`.

---

## Features

- RESTful API using Flask and Flask-RESTX
- Clean architecture (API → Services → Persistence)
- Facade pattern to decouple layers
- In-memory repository (transition to SQLAlchemy)
- JWT-based Authentication (using Flask-JWT-Extended)
- Role-based access control
- Relational modeling with SQLAlchemy:
  - One-to-many: User → Place, Place → Review
  - Many-to-many: Place ↔ Amenity
- Proper validation and error handling
- Unit tests with `unittest`

---

## Running Tests

To run unit tests:

```bash
python -m unittest discover tests
```

Tests cover all layers: API, services, and persistence.

---

## Dependencies

`requirements.txt`:

- flask
- flask-restx
- flask-jwt-extended
- sqlalchemy

---

## Future Enhancements

- Replace in-memory repo with full SQLAlchemy ORM implementation
- Add filtering and searching endpoints
- Enable pagination and sorting
- Implement user registration and login endpoints
- Add Swagger UI documentation (with Flask-RESTX)
- Deploy with Docker and Gunicorn
- Add integration and load testing

---

## Key Design Patterns Used

- **Facade Pattern**: HBnBFacade provides a unified interface to underlying services and repositories.
- **Repository Pattern**: Abstracts data access (in-memory or database) from business logic.
- **JWT Authentication**: Provides secure, stateless login/session mechanism.
- **Layered Architecture**: Promotes separation of concerns, modularity, and testability.

---

## Example Endpoints

- `GET /api/v1/places` - List all places
- `POST /api/v1/places` - Create new place (JWT required)
- `GET /api/v1/places/<place_id>` - Get place details
- `PUT /api/v1/places/<place_id>` - Update a place (ownership validated)
- `GET /api/v1/amenities` - List all amenities
- `PUT /api/v1/places/<place_id>/amenities/<amenity_id>` - Link amenity to place

---

## Authentication & Authorization

- Basic login using JWT
- Token returned after valid login
- Users can only update/delete their own resources
- Admin endpoints protected via roles

---

## Inspiration

This project is inspired by Holberton School’s HBnB architecture but redesigned for modern development practices and extensibility.

---

## Clean Code & Style

- Code follows `pycodestyle`
- Organized by responsibility and scalability
- Meaningful naming and concise documentation

---

## Author

Yoruan Orta