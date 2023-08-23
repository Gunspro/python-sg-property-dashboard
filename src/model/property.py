from sqlalchemy import Column, Integer, String, Date
from src.db.database import Base
from pydantic import BaseModel, BaseConfig
from typing import List
from datetime import datetime

class Property(Base):
    __tablename__ = "property_table"

    id = Column(String, primary_key=True, index=True)
    timestamp = Column(Date)
    price = Column(String)
    yearbuilt = Column(Integer)
    block_and_address = Column(String)
    number_of_rooms = Column(String)

class PropertyData(BaseModel):
    property_list: List[Property] 

    class Config(BaseConfig):
        arbitrary_types_allowed = True

class PropertyView(BaseModel):
    id: str
    timestamp: datetime
    price: int
    yearbuilt: int
    age: int
    block_and_address: str
    number_of_rooms: int
    area: str

class PropertyViewData(BaseModel):
    property_view_list: List[PropertyView]