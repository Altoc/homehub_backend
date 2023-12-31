from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GroceryItemDB(Base):
    __tablename__ = 'GROCERY_ITEM'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    list_id = Column(Integer, ForeignKey('GROCERY_LIST.id'), nullable=False)

class GroceryItem(BaseModel):
    name: str
    list_id: int
