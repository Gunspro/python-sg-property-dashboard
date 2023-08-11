from fastapi import Router, FastAPI
import uvicorn

app = FastAPI()

# app.include_router()
# app.include_router()

if __name__ == "__main__":
    uvicorn.run("0.0.0.0", port=9000, reload=True)