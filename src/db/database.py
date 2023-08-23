from src.utils.helper import DATABASE_URL

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

try:
    engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=10)
except:
    raise Exception("DATABASE_URL environment variable is not defined")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()