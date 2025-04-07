-- review table
USE hbnb_db;

CREATE TABLE IF NOT EXISTS reviews
(
    id CHAR(36) DEFAULT (UUID()),
    text TEXT,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    user_id CHAR(36),
    place_id CHAR(36),
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (place_id) REFERENCES places (id),
    CONSTRAINT unique_user_place UNIQUE (user_id, place_id)
);