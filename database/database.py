from databases import Database
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from app.models.grocery_list import GroceryListDB, Base

DATABASE_URL = "sqlite:///./database/data/database.db"
database = Database(DATABASE_URL)

engine = create_engine(DATABASE_URL)
metadata = MetaData()

def connect_to_database():
    """
    Connects to the database and returns a session.
    """
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_active_grocery_lists(db):
    """
    Retrieves all grocery lists with active_flag set to truthy.
    """
    return db.query(GroceryListDB).filter(GroceryListDB.active_flag == True).all()

def disconnect_from_database(db):
    """
    Disconnects from the database.
    """
    db.close()
