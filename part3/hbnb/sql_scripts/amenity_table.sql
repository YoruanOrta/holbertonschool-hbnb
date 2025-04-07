-- amenity table
USE hbnb_db;

CREATE TABLE IF NOT EXISTS amenities
(
    id CHAR(36) DEFAULT (UUID()),
    name VARCHAR(255) UNIQUE,
    PRIMARY KEY (id)
);