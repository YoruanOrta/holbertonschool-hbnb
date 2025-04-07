-- user table
USE hbnb_db;

CREATE TABLE IF NOT EXISTS users
(
    id CHAR(36) DEFAULT (UUID()),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    is_admin BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (id)
);