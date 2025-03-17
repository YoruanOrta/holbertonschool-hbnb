from flask_restx import Namespace, Resource, fields
from app.services import facade
""" API endpoints for amenities """


api = Namespace('amenities', description='Amenity operations')
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route("/")
class AmenityList(Resource):
    """Resource for creating and retrieving amenities"""
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload
        new_amenity = facade.create_amenity(amenity_data)
        return {
            'id': new_amenity.id,
            'name': new_amenity.name
        }, 201
    

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Get all amenities"""
        amenities = facade.amenity_repo.get_all()
        if not amenities:
            return {"error": "No amenities found"}, 404
        return [
            {
                'id': amenity.id,
                'name': amenity.name
            }
            for amenity in amenities
        ], 200
    

@api.route("/<amenity_id>")
class AmenityResource(Resource):
    """Resource for getting, updating and deleting amenity details"""
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return {
            'id': amenity.id,
            'name': amenity.name
        }, 200
    

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        updated_details = api.payload
        facade.update_amenity(amenity_id, updated_details)
        return {"message": "Amenity updated successfully"}, 200