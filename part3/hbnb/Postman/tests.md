# API Tests Documentation

## Users

### Create Users
**POST**  
`http://127.0.0.1:5000/api/v1/users`

**Headers:**  
- `Content-Type: application/json`

**Body Examples:**  
```json
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "password": "your_password"
}
```
```json
{
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane.doe@example.com",
    "password": "hes_password"
}
```
```json
{
    "first_name": "Mister",
    "last_name": "Admin",
    "email": "admin@example.com",
    "password": "adminpassword"
}
```

### Login
**POST**  
`http://127.0.0.1:5000/api/v1/auth/login`

**Headers:**  
- `Content-Type: application/json`

---

### Update User
**PUT**  
`http://127.0.0.1:5000/api/v1/users/<user_id>`

**Headers:**  
- `Authorization: Bearer <admin_token>`  
- `Content-Type: application/json`

**Body:**  
```json
{
    "first_name": "UpdatedFirstName",
    "last_name": "UpdatedLastName",
    "email": "updatedemail@example.com"
}
```

### Delete User
**DELETE**  
`http://127.0.0.1:5000/api/v1/users/<user_id>`

**Headers:**  
- `Authorization: Bearer <user_token>`  
- `Content-Type: application/json`

**Body:**  
`EMPTY`

---

## Places

### Create Place
**POST**  
`http://127.0.0.1:5000/api/v1/places/`

**Headers:**  
- `Authorization: Bearer <user_token>`  
- `Content-Type: application/json`

**Body:**  
```json
{
    "title": "New Place",
    "description": "A beautiful place",
    "price": 100,
    "latitude": 40.7128,
    "longitude": -74.0060,
    "owner_id": "8f95cbc7-91e3-4beb-82a5-bf5fec0a935c"
}
```

### Update Place
**PUT**  
`http://127.0.0.1:5000/api/v1/places/<place_id>`

**Headers:**  
- Same as above

**Body:**  
```json
{
    "title": "Updated Place"
}
```

### Delete Place
**DELETE**  
`http://127.0.0.1:5000/api/v1/places/<place_id>`

**Headers:**  
- `Authorization: Bearer <user_token>`  
- `Content-Type: application/json`

**Body:**  
`EMPTY`

---

## Reviews

### Create Review
**POST**  
`http://127.0.0.1:5000/api/v1/reviews/`

**Headers:**  
- `Authorization: Bearer <user_token>`  
- `Content-Type: application/json`

**Body:**  
```json
{
    "place_id": "3666f199-fd20-466d-a229-8f22cc2abb6a",
    "rating": 5,
    "text": "Great place!"
}
```

### Update Review
**PUT**  
`http://127.0.0.1:5000/api/v1/reviews/<review_id>`

**Headers:**  
- Same as above

**Body:**  
```json
{
    "text": "Updated review"
}
```

### Delete Review
**DELETE**  
`http://127.0.0.1:5000/api/v1/reviews/<review_id>`

**Headers:**  
- Same as above

**Body:**  
`EMPTY`

---

## Amenities

### Create Amenity
**POST**  
`http://127.0.0.1:5000/api/v1/amenities/`

**Headers:**  
- `Authorization: Bearer <admin_token>`  
- `Content-Type: application/json`

**Body:**  
```json
{
    "name": "Swimming Pool"
}
```

### Update Amenity
**PUT**  
`http://127.0.0.1:5000/api/v1/amenities/<amenity_id>`

**Headers:**  
- `Authorization: Bearer <admin_token>`  
- `Content-Type: application/json`

**Body:**  
```json
{
    "name": "Updated Amenity"
}
```
