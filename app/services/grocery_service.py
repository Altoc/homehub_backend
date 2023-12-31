from fastapi import Depends, APIRouter, Request
from databases import Database
from database.database import connect_to_database, get_active_grocery_lists, deactivate_grocery_list, add_items_to_grocery_list

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

@router.put("/list/edit/{list_id}")
async def edit_grocery_list_endpoint(list_id: int, request: Request, db: Database = Depends(connect_to_database)):
    # Assuming the items are in the request body as a JSON object
    request_body = await request.json()
    items = request_body.get("items", [])

    await add_items_to_grocery_list(db, list_id, items)

    return {"message": f"Grocery list edited successfully with items: {items}", "list_id": list_id}