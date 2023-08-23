from fastapi import FastAPI
import uvicorn

import subprocess
import streamlit as st
import pandas as pd

from src.controller.controller import router
from src.services.web_scraper import scrape_data, store_property_data
from src.repositories.PropertyRepository import PropertyRepository
from src.db.database import SessionLocal

app = FastAPI()

app.include_router(router)

@app.on_event("startup")
async def startup_event():
    df = scrape_data()
    store_property_data(df)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)



