from app.persistence.repository import SQLAlchemyRepository
from app.models.place import Place

class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)
