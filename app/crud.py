from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: schemas.user.UserUpdate):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.username:
        user.username = user_update.username
    if user_update.email:
        user.email = user_update.email
    if user_update.password:
        user.hashed_password = pwd_context.hash(user_update.password)

    db.commit()
    db.refresh(user)
    return user


def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()


def get_categories(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Category).offset(skip).limit(limit).all()


def create_expense(db: Session, expense: schemas.ExpenseCreate, user_id: int):
    db_expense = models.Expense(**expense.dict(), user_id=user_id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def get_expenses_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Expense).filter(models.Expense.user_id == user_id).offset(skip).limit(limit).all()


def get_expense(db: Session, expense_id: int):
    return db.query(models.Expense).filter(models.Expense.id == expense_id).first()


def update_expense(db: Session, expense_id: int, expense: schemas.ExpenseCreate):
    db_expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db_expense.amount = expense.amount
    db_expense.description = expense.description
    db_expense.date = expense.date
    db_expense.category_id = expense.category_id

    db.commit()
    db.refresh(db_expense)
    return db_expense


def delete_expense(db: Session, expense_id: int):
    db_expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(db_expense)
    db.commit()
    return db_expense


def create_budget(db: Session, budget: schemas.BudgetCreate, user_id: int):
    db_budget = models.Budget(**budget.dict(), user_id=user_id)
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget


def get_budget(db: Session, budget_id: int):
    return db.query(models.Budget).filter(models.Budget.id == budget_id).first()


def get_budgets_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Budget).filter(models.Budget.user_id == user_id).offset(skip).limit(limit).all()
