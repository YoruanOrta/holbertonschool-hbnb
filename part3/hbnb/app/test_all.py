import unittest
from app import create_app
""" Import the create_app function from the app module """

class TestAPIEndpoints(unittest.TestCase):
    """ Test the API endpoints """

    def setUp(self):
        """ Set up the test client """
        self.app = create_app(testing=True)
        self.client = self.app.test_client()

    def test_create_amenity(self):
        """Test creating a new amenity"""
        response = self.client.post('/api/v1/amenities/', json={"name": "Wi-Fi"})
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    def test_get_all_amenities(self):
        """Test getting all amenities"""
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_amenity(self):
        """Test getting an amenity by its ID"""
        create_response = self.client.post('/api/v1/amenities/', json={"name": "Wi-Fi"})
        amenity_id = create_response.json['id']
        
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Wi-Fi")

    def test_create_user(self):
        """Test creating a new user"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    def test_get_user(self):
        """Test getting a user by their ID"""
        create_response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith@example.com"
        })
        user_id = create_response.json['id']

        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], "john.smith@example.com")

    def test_get_user_not_found(self):
        """Test getting a nonexistent user"""
        response = self.client.get('/api/v1/users/nonexistent-id')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'User not found')

    def test_create_place(self):
        """Test creating a new place"""
        response = self.client.post('/api/v1/places/', json={
            "name": "Beach House",
            "city": "Santa Monica"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    def test_get_place(self):
        """Test getting a place by its ID"""
        create_response = self.client.post('/api/v1/places/', json={
            "name": "Mountain Cabin",
            "city": "Aspen"
        })
        place_id = create_response.json['id']
        
        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Mountain Cabin")

    def test_create_review(self):
        """Test creating a new review"""
        response = self.client.post('/api/v1/reviews/', json={
            "place_id": "someplace-id",
            "user_id": "someuser-id",
            "rating": 5,
            "comment": "Amazing place!"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)
