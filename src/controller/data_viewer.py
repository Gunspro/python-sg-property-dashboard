from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from src.repositories.PropertyRepository import PropertyRepository
from src.db.database import SessionLocal
from src.model.property import PropertyData
from src.db.database import SessionLocal
from src.services import data_transformation 

router = APIRouter()

@router.get("/properties")
def get_all_properties():
    db = SessionLocal()
    propertyRepo = PropertyRepository(db)
    properties = propertyRepo.get_properties()
    
    property_data = []

    for props in properties:
        props.block_and_address = data_transformation.transform_block_and_address(props.block_and_address)
        props.number_of_rooms = data_transformation.transform_no_of_rooms(props.number_of_rooms)
        
        property_data.append({
            "id": props.id,
            "timestamp": props.timestamp,
            "price": props.price,
            "yearbuilt": props.yearbuilt,
            "block_and_address": props.block_and_address,
            "number_of_rooms": props.number_of_rooms
        })

    return property_data

