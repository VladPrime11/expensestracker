from pydantic import BaseModel
from datetime import date

class ExpenseBase(BaseModel):
    amount: float
    description: str
    date: date
    category_id: int

class ExpenseCreate(ExpenseBase):
    pass

class Expense(ExpenseBase):
    id: int

    class Config:
        from_attributes = True
