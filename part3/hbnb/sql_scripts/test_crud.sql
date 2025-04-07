-- testing CRUD operations
USE hbnb_db;

-- Create
INSERT INTO users (first_name, last_name, email, password)
VALUES (
    'John',
    'Doe',
    'john.doe@example.com',
    'your_password'
);

-- Read
SELECT * FROM users;

SELECT * FROM amenities;

-- Update
UPDATE users
SET first_name = 'Jane'
WHERE email = 'john.doe@example.com';

-- Delete
DELETE FROM amenities
WHERE name = 'Swimming Pool';


-- Verify all changes
SELECT * FROM users;

SELECT * FROM amenities;