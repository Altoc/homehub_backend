from pydantic import BaseModel
from datetime import date

class GroceryList(BaseModel):
    date: date
    name: str
    active: bool