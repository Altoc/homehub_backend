from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.services.grocery_service import router as grocery_router

app = FastAPI()

# Allow requests from all origins (adjust as needed for security)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(grocery_router, prefix="/api/grocery")

@app.get("/")
def read_root():
    return {"Hello": "World"}