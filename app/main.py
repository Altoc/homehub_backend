from fastapi import FastAPI
from app.services.grocery_service import router as grocery_router

app = FastAPI()

app.include_router(grocery_router, prefix="/api/grocery")

@app.get("/")
def read_root():
    return {"Hello": "World"}