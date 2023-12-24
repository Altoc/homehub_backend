from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import date

Base = declarative_base()

class GroceryListDB(Base):
    __tablename__ = 'GROCERY_LIST'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    date = Column(Text, nullable=False)
    active_flag = Column(Boolean, nullable=False)

class GroceryList(BaseModel):
    date: date
    name: str
    active: bool