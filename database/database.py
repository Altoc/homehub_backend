from databases import Database
from sqlalchemy import create_engine, MetaData, select
import logging
from app.models.grocery_list import GroceryListDB, Base
from app.models.grocery_item import GroceryItemDB, Base

DATABASE_URL = "sqlite:///./database/data/database.db"
# database = Database(DATABASE_URL)

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

engine = create_engine(DATABASE_URL, echo=True)
dialect = engine.dialect
metadata = MetaData()

async def connect_to_database():
    """
    Connects to the database and returns a connection.
    """
    db = Database(DATABASE_URL)
    await db.connect()
    try:
        print("Connecting to DB...")
        yield db
    finally:
        print("Disconnecting From DB...")
        await db.disconnect()

async def get_active_grocery_lists(db):
    """
    Retrieves all grocery lists with active_flag set to truthy.
    """
    query = GroceryListDB.__table__.select().where(GroceryListDB.__table__.c.active_flag == True)
    result = await db.fetch_all(query)
    return result

async def deactivate_grocery_list(db, list_id):
    """
    Sets a given list_id active_flag state to FALSE.
    This effectively "deletes" the record from user perspective.
    """
    # Assuming you have a SQLAlchemy model named GroceryListDB
    query = GroceryListDB.__table__.update().where(GroceryListDB.__table__.c.id == list_id).values(active_flag=False)
    await db.execute(query)

    # Optionally, you can return the updated record or a success message
    updated_grocery_list = await db.fetch_one(GroceryListDB.__table__.select().where(GroceryListDB.__table__.c.id == list_id))
    return updated_grocery_list

async def add_items_to_grocery_list(db, list_id: int, items: list):
    """
    Adds items to a grocery list identified by list_id.
    """
    try:
        # Check if the grocery list exists
        query = select(GroceryListDB).where(GroceryListDB.id == list_id)
        grocery_list = await db.fetch_one(query)

        if grocery_list:
            # Assuming you have a table object defined for GroceryItemDB
            grocery_item_table = GroceryItemDB.__table__

            # Create GroceryItemDB instances for the new items
            new_items = [{"name": item, "list_id": list_id} for item in items]

            # Get the compiled SQL statement and parameters
            insert_query = grocery_item_table.insert().values(new_items)
            compiled_query = insert_query.compile()
            compiled_sql = str(compiled_query)
            parameters = [item for sublist in new_items for item in sublist.values()]

            logger.debug("Insert query: %s", compiled_sql)
            logger.debug("Parameters: %s", parameters)

            # Insert the new items into the GROCERY_ITEM table
            await db.execute(insert_query)

            # Commit the changes
            # await db.commit()

            return {"message": "Items added to grocery list successfully"}

        return {"message": "Grocery list not found"}

    except Exception as e:
        return {"error": str(e)}

async def disconnect_from_database(db):
    """
    Disconnects from the database.
    """
    print("Disonnecting From DB...")
    await db.disconnect()
