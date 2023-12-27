from fastapi import Depends, APIRouter
from typing import Union
from datetime import date
import asyncio
from databases import Database
from database.database import connect_to_database, get_active_grocery_lists, deactivate_grocery_list
from app.models.grocery_list import Base, GroceryList

router = APIRouter()

# Dependency to get the database session
#async def get_db():
#    loop = asyncio.get_event_loop()
#    return await loop.run_in_executor(None, connect_to_database)

# Route to retrieve active grocery lists
@router.get("/list/active_grocery_lists")
async def read_active_grocery_lists_endpoint(db: Database = Depends(connect_to_database)):
    active_grocery_lists = await get_active_grocery_lists(db)
    return {"active_grocery_lists": active_grocery_lists}

# Route to deactivate a grocery list
@router.put("/list/deactivate/{list_id}")
async def deactivate_grocery_list_endpoint(list_id: int, db: Database = Depends(connect_to_database)):
    updated_grocery_list = await deactivate_grocery_list(db, list_id)
    if updated_grocery_list:
        return {"message": "Grocery list state updated successfully", "updated_grocery_list": updated_grocery_list}
    else:
        raise HTTPException(status_code=404, detail="Grocery list not found")

@router.post("/list")
def create_grocery_list(grocery_list: GroceryList):
    # In a real application, you might want to store the created grocery list in a database.
    # For simplicity, we'll just return the received data in the response.
    return {"message": "Grocery list created successfully", "grocery_list": grocery_list}