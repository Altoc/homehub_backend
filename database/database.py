from databases import Database
from sqlalchemy import func, create_engine, MetaData, select, join
from datetime import datetime
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
    join_condition = GroceryListDB.__table__.c.id == GroceryItemDB.__table__.c.list_id
    query = select([GroceryListDB, GroceryItemDB]).select_from(join(GroceryListDB.__table__, GroceryItemDB.__table__, join_condition)).where(GroceryListDB.__table__.c.active_flag == True)
    
    ## query = GroceryListDB.__table__.select().where(GroceryListDB.__table__.c.active_flag == True)
    rows = await db.fetch_all(query)
    result = []
    for row in rows:
        if(result and result[-1][0] == row[0]):
            result_row = result[-1]
        else:
            result_row = []
            #grocery_list info
            result_row.append(row[0]) #grocery_list.id
            result_row.append(row[1]) #grocery_list.name
            result_row.append(row[2]) #grocery_list.date
            # result_row.append(row[3]) #grocery_list.active_flag
            result.append(result_row)
        #grocery_item info
        result_row.append([row[4], row[5]]) #grocery_item.id, grocery_item.name
        print(result_row)
    return result

async def create_grocery_list(db, name: str, items: list):
    """
    Create a new grocery list.

    Note: items is not used rn. Can use it later if you want to add items as you create list.
    """
    try:
        # Create a new grocery list with the current date
        query = GroceryListDB.__table__.insert().values(name=name, date=func.now(), active_flag=True)
        await db.execute(query)

        # Get the current date in ISO format
        current_date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        return {"created_at": current_date, "message": "Grocery list created successfully"}

    except Exception as e:
        return {"error": str(e)}

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
