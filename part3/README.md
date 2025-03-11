Part 3: Enhanced Backend with Authentication and Database Integration
Welcome to Part 3 of the HBnB Project, where you will extend the backend of the application by introducing user authentication, authorization, and database integration using SQLAlchemy and SQLite for development. Later, you’ll configure MySQL for production environments. In this part, you will secure the backend, introduce persistent storage, and prepare the application for a scalable, real-world deployment.

Objectives of the Project
Authentication and Authorization: Implement JWT-based user authentication using Flask-JWT-Extended and role-based access control with the is_admin attribute for specific endpoints.
Database Integration: Replace in-memory storage with SQLite for development using SQLAlchemy as the ORM and prepare for MySQL or other production grade RDBMS.
CRUD Operations with Database Persistence: Refactor all CRUD operations to interact with a persistent database.
Database Design and Visualization: Design the database schema using mermaid.js and ensure all relationships between entities are correctly mapped.
Data Consistency and Validation: Ensure that data validation and constraints are properly enforced in the models.
Learning Objectives
By the end of this part, you will:

Implement JWT authentication to secure your API and manage user sessions.
Enforce role-based access control to restrict access based on user roles (regular users vs. administrators).
Replace in-memory repositories with a SQLite-based persistence layer using SQLAlchemy for development and configure MySQL for production.
Design and visualize a relational database schema using mermaid.js to handle relationships between users, places, reviews, and amenities.
Ensure the backend is secure, scalable, and provides reliable data storage for production environments.
Project Context
In the previous parts of the project, you worked with in-memory storage, which is ideal for prototyping but insufficient for production environments. In Part 3, you’ll transition to SQLite, a lightweight relational database, for development, while preparing the system for MySQL in production. This will give you hands-on experience with real-world database systems, allowing your application to scale effectively.

Additionally, you’ll introduce JWT-based authentication to secure the API, ensuring that only authenticated users can interact with certain endpoints. You will also implement role-based access control to enforce restrictions based on the user’s privileges (regular users vs. administrators).

Project Resources
Here are some resources that will guide you through this part of the project:

JWT Authentication: Flask-JWT-Extended Documentation
SQLAlchemy ORM: SQLAlchemy Documentation
SQLite: SQLite Documentation
Flask Documentation: Flask Official Documentation
Mermaid.js for ER Diagrams: Mermaid.js Documentation
Structure of the Project
In this part of the project, the tasks are organized in a way that builds progressively towards a complete, secure, and database-backed backend system:

Modify the User Model to Include Password: You will start by modifying the User model to store passwords securely using bcrypt2 and update the user registration logic.
Implement JWT Authentication: Secure the API using JWT tokens, ensuring only authenticated users can access protected endpoints.
Implement Authorization for Specific Endpoints: You will implement role-based access control to restrict certain actions (e.g., admin-only actions).
SQLite Database Integration: Transition from in-memory data storage to SQLite as the persistent database during development.
Map Entities Using SQLAlchemy: Map existing entities (User, Place, Review, Amenity) to the database using SQLAlchemy and ensure relationships are well-defined.
Prepare for MySQL in Production: Towards the end of this phase, you’ll configure the application to use MySQL in production and SQLite for development.
Database Design and Visualization: Use mermaid.js to create entity-relationship diagrams for your database schema.
Each task is carefully designed to build on previous work and ensure the system transitions smoothly from development to production readiness.

By the end of Part 3, you will have a backend that not only stores data in a persistent and secure database but also ensures that only authorized users can access and modify specific data. You will have implemented industry-standard authentication and database management practices that are crucial for real-world web applications.