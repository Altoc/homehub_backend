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

async def disconnect_from_database(db):
    """
    Disconnects from the database.
    """
    print("Disonnecting From DB...")
    await db.disconnect()
