from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from . import models, crud, auth
from .models import SessionLocal, engine
from .auth import get_current_active_user, get_current_active_admin
from .deps import get_db
from .schemas import User, UserCreate, UserUpdate, Expense, ExpenseCreate, Category, CategoryCreate, Token, Budget, BudgetCreate

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes for expenses
@app.post("/expenses/", response_model=Expense)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_active_user)):
    return crud.create_expense(db=db, expense=expense, user_id=current_user.id)

@app.get("/expenses/", response_model=list[Expense])
def read_expenses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_active_user)):
    expenses = crud.get_expenses_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return expenses

@app.get("/expenses/{expense_id}", response_model=Expense)
def read_expense(expense_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_active_user)):
    db_expense = crud.get_expense(db, expense_id=expense_id)
    if db_expense is None or db_expense.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense

@app.put("/expenses/{expense_id}", response_model=Expense)
def update_expense(expense_id: int, expense: ExpenseCreate, db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_active_user)):
    db_expense = crud.update_expense(db, expense_id=expense_id, expense=expense)
    if db_expense is None or db_expense.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense

@app.delete("/expenses/{expense_id}", response_model=Expense)
def delete_expense(expense_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_active_user)):
    db_expense = crud.delete_expense(db, expense_id=expense_id)
    if db_expense is None or db_expense.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense

# User registration
@app.post("/register/", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

# User login
@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Get current user
@app.get("/users/me/", response_model=User)
def read_users_me(current_user: User = Depends(auth.get_current_active_user)):
    return current_user

@app.put("/users/me/", response_model=User)
def update_user_me(user_update: UserUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    updated_user = crud.update_user(db, current_user.id, user_update)
    return updated_user

# Get current admin
@app.get("/users/me/admin/", response_model=User)
def read_users_me_admin(current_user: User = Depends(auth.get_current_active_admin)):
    return current_user

@app.post("/categories/", response_model=Category)
def create_category(category: CategoryCreate, db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_active_user)):
    return crud.create_category(db, category)

@app.get("/categories/", response_model=list[Category])
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_categories(db, skip=skip, limit=limit)

# Routes for budgets
@app.post("/budgets/", response_model=Budget)
def create_budget(budget: BudgetCreate, db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_active_user)):
    return crud.create_budget(db=db, budget=budget, user_id=current_user.id)

@app.get("/budgets/", response_model=list[Budget])
def read_budgets(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_active_user)):
    budgets = crud.get_budgets_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return budgets

@app.get("/budgets/{budget_id}", response_model=Budget)
def read_budget(budget_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_active_user)):
    db_budget = crud.get_budget(db, budget_id=budget_id)
    if db_budget is None or db_budget.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Budget not found")
    return db_budget
