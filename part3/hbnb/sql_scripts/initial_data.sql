-- populate the tables with initial data
USE hbnb_db;

INSERT INTO users (id, email, first_name, last_name, password, is_admin)
VALUES (
    '8f95cbc7-91e3-4beb-82a5-bf5fec0a935c',
    'john.doe@example.com',
    'John',
    'Doe',
    'your_password',
    True
    );

INSERT INTO amenities (name)
VALUES ('WiFi'), ('Swimming Pool'), ('Air Conditioning');