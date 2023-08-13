from sqlalchemy import Column, Integer, String
from src.db.database import Base
from pydantic import BaseModel, BaseConfig
from typing import List

class Property(Base):
    __tablename__ = "property_table"

    id = Column(Integer, primary_key=True, index=True)
    price = Column(String)
    yearbuilt = Column(Integer)
    block_and_address = Column(String)
    number_of_rooms = Column(String)

class PropertyData(BaseModel):
    property_list: List[Property] 

    class Config(BaseConfig):
        arbitrary_types_allowed = True