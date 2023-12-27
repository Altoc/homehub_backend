from databases import Database
from sqlalchemy import create_engine, MetaData
from app.models.grocery_list import GroceryListDB, Base

DATABASE_URL = "sqlite:///./database/data/database.db"
database = Database(DATABASE_URL)

engine = create_engine(DATABASE_URL)
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


async def disconnect_from_database(db):
    """
    Disconnects from the database.
    """
    print("Disonnecting From DB...")
    await db.disconnect()
