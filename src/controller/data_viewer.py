from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from src.repositories.PropertyRepository import PropertyRepository
from src.db.database import SessionLocal
from src.model.property import PropertyView
from src.db.database import SessionLocal
from src.services import data_transformation

router = APIRouter()

@router.get("/properties")
def get_all_properties():
    db = SessionLocal()
    propertyRepo = PropertyRepository(db)
    properties = propertyRepo.get_properties()

    property_view_data = []

    for props in properties:
        props.block_and_address = data_transformation.transform_block_and_address(props.block_and_address)
        props.number_of_rooms = data_transformation.transform_no_of_rooms(props.number_of_rooms)
        if props.price.startswith("$"):
            props.price = int("".join(filter(str.isdigit, props.price)))
        else:
            props.price = data_transformation.transform_price(properties, props.block_and_address, props.price, props.number_of_rooms)
        
        props.floor_size = data_transformation.transform_floorsize(props.floor_size)
        age = data_transformation.transform_yearbuilt(props.yearbuilt)
        area = data_transformation.assign_location(props.block_and_address).lower()
        
        property_view_model = PropertyView(**props.__dict__, age = age, area = area)
        property_view_data.append(property_view_model)

    return property_view_data