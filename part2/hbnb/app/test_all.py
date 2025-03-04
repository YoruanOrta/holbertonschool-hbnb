import unittest
from app import create_app

class TestAPIEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app(testing=True)
        self.client = self.app.test_client()

    def test_create_amenity(self):
        """Test crear una nueva amenidad"""
        response = self.client.post('/api/v1/amenities/', json={"name": "Wi-Fi"})
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    def test_get_all_amenities(self):
        """Test obtener todas las amenidades"""
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_amenity(self):
        """Test obtener una amenidad por su ID"""
        create_response = self.client.post('/api/v1/amenities/', json={"name": "Wi-Fi"})
        amenity_id = create_response.json['id']
        
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Wi-Fi")

    def test_create_user(self):
        """Test crear un nuevo usuario"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    def test_get_user(self):
        """Test obtener un usuario por su ID"""
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
        """Test obtener un usuario inexistente"""
        response = self.client.get('/api/v1/users/nonexistent-id')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'User not found')

    def test_create_place(self):
        """Test crear un nuevo lugar"""
        response = self.client.post('/api/v1/places/', json={
            "name": "Beach House",
            "city": "Santa Monica"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    def test_get_place(self):
        """Test obtener un lugar por su ID"""
        create_response = self.client.post('/api/v1/places/', json={
            "name": "Mountain Cabin",
            "city": "Aspen"
        })
        place_id = create_response.json['id']
        
        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Mountain Cabin")

    def test_create_review(self):
        """Test crear una nueva reseña"""
        response = self.client.post('/api/v1/reviews/', json={
            "place_id": "someplace-id",
            "user_id": "someuser-id",
            "rating": 5,
            "comment": "Amazing place!"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

if __name__ == '__main__':
    unittest.main()