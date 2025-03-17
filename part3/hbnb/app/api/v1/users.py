from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request, jsonify
""" API endpoints for user management """

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

@api.route('/')
class UserList(Resource):
    """Resource for user list"""
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve all users"""
        users = facade.get_all_users()
        user_list = [
            {
                'id': user.id, 
                'first_name': user.first_name, 
                'last_name': user.last_name, 
                'email': user.email
            } 
            for user in users
        ]
        return user_list, 200

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        from app import bcrypt

        user_data = api.payload

        # Check if email is already registered
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:

            # Create user with hashed password
            new_user = facade.create_user(user_data)
            

            # Return only user ID and success message
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email,
                }, 201

        except ValueError as e:
            return {'error': 'Invalid input data'}, 400

@api.route('/<user_id>')
class UserResource(Resource):
    """Resource for user details"""
    
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Explicitly exclude password from the response
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update user details"""
        user_data = api.payload

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user and existing_user.id != user_id:
            return {'error': 'Email already registered'}, 400

        try:
            updated_user = facade.update_user(user_id, user_data)
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name, 
                'last_name': updated_user.last_name, 
                'email': updated_user.email
            }, 200
        
        except ValueError as e:
            return {'error': 'Invalid input data'}, 400

    @api.response(200, 'User deleted successfully')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """Delete a user by ID"""
        try:
            return facade.delete_user(user_id)
        except ValueError as e:
            return {"error": str(e)}, 404