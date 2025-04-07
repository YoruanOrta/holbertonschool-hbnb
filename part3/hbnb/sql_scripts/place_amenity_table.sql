-- place_amenity table
USE hbnb_db;

CREATE TABLE IF NOT EXISTS place_amenity
(
    place_id CHAR(36) DEFAULT (UUID()),
    amenity_id CHAR(36),
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places (id),
    FOREIGN KEY (amenity_id) REFERENCES amenities (id)
);