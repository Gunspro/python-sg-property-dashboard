from typing import List
from sqlalchemy.orm import Session
from src.model.property import Property
from sqlalchemy import or_

class PropertyRepository:
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_properties(self):
        return self.db.query(Property).all()

    def get_properties_by_address(self, address: str):
        search_condition = or_(
            Property.block_and_address.ilike(f"%{address}%"),  # Case-insensitive search on the 'name' column
        )
        return self.db.query(Property).filter(search_condition).all()
    
    def create_properties(self, properties: List[Property]):
        property_instances = [Property(**item) for item in properties]  # Use 'properties' parameter
        self.db.bulk_save_objects(property_instances)
        self.db.commit()
        return properties

    def truncate_properties(self):
        query = text("TRUNCATE TABLE property_table")
        self.db.execute(query)
        self.db.commit()
