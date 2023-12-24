from fastapi import Depends, APIRouter
from typing import Union
from datetime import date
from sqlalchemy.orm import Session
from database.database import connect_to_database, get_active_grocery_lists
from app.models.grocery_list import Base, GroceryList

router = APIRouter()

# Dependency to get the database session
def get_db():
    with connect_to_database() as db:
        yield db

# Route to retrieve active grocery lists
@router.get("/list/active_grocery_lists")
def read_active_grocery_lists(db: Session = Depends(get_db)):
    active_grocery_lists = get_active_grocery_lists(db)
    return {"active_grocery_lists": active_grocery_lists}

@router.get("/list/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    """
    Returns a grocery list for a given user.
    If no user is supplied, returns all grocery lists.
    """
    grocery_list_data = {
        "date": date.today(),
        "name": "Example Grocery List",
        "active": True
    }
    return GroceryList(**grocery_list_data)

@router.put("/list/{item_id}")
def update_grocery_list(item_id: int, grocery_list: GroceryList):
    return {"grocery_list_name": grocery_list.name, "grocery_list_id": item_id}

@router.post("/list")
def create_grocery_list(grocery_list: GroceryList):
    # In a real application, you might want to store the created grocery list in a database.
    # For simplicity, we'll just return the received data in the response.
    return {"message": "Grocery list created successfully", "grocery_list": grocery_list}