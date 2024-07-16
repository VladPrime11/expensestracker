# app/schemas.py

from datetime import date
from pydantic import BaseModel

class ExpenseBase(BaseModel):
    amount: float
    description: str
    category: str
    date: date

class ExpenseCreate(ExpenseBase):
    pass

class Expense(ExpenseBase):
    id: int

    class Config:
        orm_mode = True
