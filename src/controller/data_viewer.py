from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from src.repositories.PropertyRepository import PropertyRepository
from src.db.database import SessionLocal
from src.model.property import PropertyData

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

