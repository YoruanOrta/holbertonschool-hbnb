-- place table
USE hbnb_db;

CREATE TABLE IF NOT EXISTS places
(
    id CHAR(36) DEFAULT (UUID()),
    title VARCHAR(255),
    description TEXT,
    price DECIMAL(10, 2),
    latitude FLOAT,
    longitude FLOAT,
    owner_id CHAR(36),
    PRIMARY KEY (id),
    FOREIGN KEY (owner_id) REFERENCES users (id)
);