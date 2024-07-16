# app/crud.py

from sqlalchemy.orm import Session
from . import models, schemas

def get_expenses(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Expense).offset(skip).limit(limit).all()

def get_expense(db: Session, expense_id: int):
    return db.query(models.Expense).filter(models.Expense.id == expense_id).first()

def create_expense(db: Session, expense: schemas.ExpenseCreate):
    db_expense = models.Expense(**expense.dict())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

def delete_expense(db: Session, expense_id: int):
    db_expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    db.delete(db_expense)
    db.commit()
    return db_expense

def update_expense(db: Session, expense_id: int, expense: schemas.ExpenseCreate):
    db_expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if db_expense:
        db_expense.amount = expense.amount
        db_expense.description = expense.description
        db_expense.category = expense.category
        db_expense.date = expense.date
        db.commit()
        db.refresh(db_expense)
    return db_expense
