from sqlalchemy.orm import Session
from passlib.context import CryptContext

from . import models, schemas
from .models import User
from .schemas import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user