from sqlalchemy import Column, Integer, String
from src.db.database import Base
from pydantic import BaseModel
from typing import List

class Property(Base):
    __tablename__ = "property"

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Integer)
    yearbuilt = Column(Integer)
    block_and_address = Column(String)
    number_of_rooms = Column(String)

class PropertyData(BaseModel):
    property_list: List[Property] 
