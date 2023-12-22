from fastapi import APIRouter
from typing import Union
from app.models.grocery_list import Item

router = APIRouter()

@router.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@router.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@router.post("/items")
def create_item(item: Item):
    # In a real application, you might want to store the created item in a database.
    # For simplicity, we'll just return the received data in the response.
    return {"message": "Item created successfully", "item": item}