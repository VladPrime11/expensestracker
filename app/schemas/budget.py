from pydantic import BaseModel
from datetime import date

class BudgetBase(BaseModel):
    amount: float
    category_id: int
    start_date: date
    end_date: date

class BudgetCreate(BudgetBase):
    pass

class Budget(BudgetBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
