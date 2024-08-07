# Expense Tracker API

Expense Tracker API is a RESTful service built with FastAPI for managing personal expenses. This project allows users to register, authenticate, create and manage expenses, categories, and budgets. It also includes features for tracking expenses and receiving budget notifications.

## Features

- User registration and authentication
- CRUD operations for expenses
- Category management
- Budget setting and tracking
- JWT token-based authentication
- API documentation with Swagger UI

## Table of Contents

- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Contributing](#contributing)


## Installation

1. **Clone the repository**

    ```bash
    git clone https://github.com/VladPrime11/expensestracker.git
    cd expense-tracker
    ```

2. **Create and activate a virtual environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the migrations**

    ```bash
    alembic upgrade head
    ```

5. **Start the FastAPI server**

    ```bash
    uvicorn app.main:app --reload
    ```

6. **Access the API documentation**

    Open your browser and navigate to `http://127.0.0.1:8000/docs` to see the interactive API documentation provided by Swagger.

## Running the Application

1. **Run the migrations**

    Apply the database migrations to set up the initial database schema.

    ```bash
    alembic upgrade head
    ```

2. **Start the application**

    Run the FastAPI application using Uvicorn.

    ```bash
    uvicorn app.main:app --reload
    ```

    The `--reload` flag will auto-reload the server if there are any code changes.

3. **Access the application**

    Open your web browser and go to `http://127.0.0.1:8000`.

4. **Interactive API documentation**

    FastAPI provides interactive API documentation out of the box. You can access it at:

    - Swagger UI: `http://127.0.0.1:8000/docs`
    - ReDoc: `http://127.0.0.1:8000/redoc`

5. **Environment Variables**

    Make sure to set up any necessary environment variables for your application. You can use a `.env` file to store these variables. For example:

    ```plaintext
    DATABASE_URL=sqlite:///./test.db
    SECRET_KEY=config.SECRET_KEY
    ACCESS_TOKEN_EXPIRE_MINUTES=600
    ```

    Load these variables in your application using `python-dotenv` or a similar library.

6. **Create a Superuser (Optional)**

    If your application has user authentication and you want to create a superuser for testing purposes, you can do so via the command line or by adding a route in your application for this purpose.

Following these steps will help you run your FastAPI application locally for development and testing purposes.


## API Endpoints

### Authentication

- **Register a new user**

    ```http
    POST /register/
    ```

    **Request Body:**

    ```json
    {
        "username": "your_username",
        "email": "your_email@example.com",
        "password": "your_password"
    }
    ```

    **Response:**

    ```json
    {
        "id": 1,
        "username": "your_username",
        "email": "your_email@example.com",
        "is_active": true,
        "is_admin": false
    }
    ```

- **Login to get access token**

    ```http
    POST /token
    ```

    **Request Body:**

    ```json
    {
        "username": "your_username",
        "password": "your_password"
    }
    ```

    **Response:**

    ```json
    {
        "access_token": "your_access_token",
        "token_type": "bearer"
    }
    ```

### User Management

- **Get current user**

    ```http
    GET /users/me/
    ```

    **Response:**

    ```json
    {
        "id": 1,
        "username": "your_username",
        "email": "your_email@example.com",
        "is_active": true,
        "is_admin": false
    }
    ```

- **Update current user**

    ```http
    PUT /users/me/
    ```

    **Request Body:**

    ```json
    {
        "username": "new_username",
        "email": "new_email@example.com",
        "password": "new_password"
    }
    ```

    **Response:**

    ```json
    {
        "id": 1,
        "username": "new_username",
        "email": "new_email@example.com",
        "is_active": true,
        "is_admin": false
    }
    ```

### Expenses

- **Create a new expense**

    ```http
    POST /expenses/
    ```

    **Request Body:**

    ```json
    {
        "amount": 100.0,
        "description": "Grocery shopping",
        "date": "2024-07-16",
        "category_id": 1
    }
    ```

    **Response:**

    ```json
    {
        "id": 1,
        "amount": 100.0,
        "description": "Grocery shopping",
        "date": "2024-07-16",
        "user_id": 1,
        "category_id": 1
    }
    ```

- **Get all expenses**

    ```http
    GET /expenses/
    ```

    **Response:**

    ```json
    [
        {
            "id": 1,
            "amount": 100.0,
            "description": "Grocery shopping",
            "date": "2024-07-16",
            "user_id": 1,
            "category_id": 1
        }
    ]
    ```

- **Get a specific expense**

    ```http
    GET /expenses/{expense_id}
    ```

    **Response:**

    ```json
    {
        "id": 1,
        "amount": 100.0,
        "description": "Grocery shopping",
        "date": "2024-07-16",
        "user_id": 1,
        "category_id": 1
    }
    ```

- **Update an expense**

    ```http
    PUT /expenses/{expense_id}
    ```

    **Request Body:**

    ```json
    {
        "amount": 150.0,
        "description": "Updated grocery shopping",
        "date": "2024-07-17",
        "category_id": 1
    }
    ```

    **Response:**

    ```json
    {
        "id": 1,
        "amount": 150.0,
        "description": "Updated grocery shopping",
        "date": "2024-07-17",
        "user_id": 1,
        "category_id": 1
    }
    ```

- **Delete an expense**

    ```http
    DELETE /expenses/{expense_id}
    ```

    **Response:**

    ```json
    {
        "id": 1,
        "amount": 100.0,
        "description": "Grocery shopping",
        "date": "2024-07-16",
        "user_id": 1,
        "category_id": 1
    }
    ```

### Categories

- **Create a new category**

    ```http
    POST /categories/
    ```

    **Request Body:**

    ```json
    {
        "name": "Groceries"
    }
    ```

    **Response:**

    ```json
    {
        "id": 1,
        "name": "Groceries"
    }
    ```

- **Get all categories**

    ```http
    GET /categories/
    ```

    **Response:**

    ```json
    [
        {
            "id": 1,
            "name": "Groceries"
        }
    ]
    ```

### Budgets

- **Create a new budget**

    ```http
    POST /budgets/
    ```

    **Request Body:**

    ```json
    {
        "amount": 1000.0,
        "category_id": 1,
        "month": 7,
        "year": 2024
    }
    ```

    **Response:**

    ```json
    {
        "id": 1,
        "amount": 1000.0,
        "category_id": 1,
        "month": 7,
        "year": 2024,
        "user_id": 1
    }
    ```

- **Get all budgets**

    ```http
    GET /budgets/
    ```

    **Response:**

    ```json
    [
        {
            "id": 1,
            "amount": 1000.0,
            "category_id": 1,
            "month": 7,
            "year": 2024,
            "user_id": 1
        }
    ]
    ```

- **Get a specific budget**

    ```http
    GET /budgets/{budget_id}
    ```

    **Response:**

    ```json
    {
        "id": 1,
        "amount": 1000.0,
        "category_id": 1,
        "month": 7,
        "year": 2024,
        "user_id": 1
    }
    ```

- **Update a budget**

    ```http
    PUT /budgets/{budget_id}
    ```

    **Request Body:**

    ```json
    {
        "amount": 1200.0,
        "category_id": 1,
        "month": 7,
        "year": 2024
    }
    ```

    **Response:**

    ```json
    {
        "id": 1,
        "amount": 1200.0,
        "category_id": 1,
        "month": 7,
        "year": 2024,
        "user_id": 1
    }
    ```

- **Delete a budget**

    ```http
    DELETE /budgets/{budget_id}
    ```

    **Response:**

    ```json
    {
        "id": 1,
        "amount": 1000.0,
        "category_id": 1,
        "month": 7,
        "year": 2024,
        "user_id": 1
    }
    ```

Этот раздел включает описание всех основных конечных точек API, их пути, запросы и ответы.


## Testing

To test the API, you can use Postman. Follow these steps to set up and test:

### 1. Install Postman

If you haven't already installed Postman, download and install it from the official website: [Postman](https://www.postman.com/downloads/).

### 2. Import Postman Collection

1. Create a new collection in Postman.
2. Add requests for all available API endpoints:
    - User Registration (POST `/register/`)
    - User Login (POST `/token`)
    - Get Current User (GET `/users/me/`)
    - Update Current User (PUT `/users/me/`)
    - Create Category (POST `/categories/`)
    - Get All Categories (GET `/categories/`)
    - Create Expense (POST `/expenses/`)
    - Get All Expenses (GET `/expenses/`)
    - Get Expense by ID (GET `/expenses/{expense_id}`)
    - Update Expense (PUT `/expenses/{expense_id}`)
    - Delete Expense (DELETE `/expenses/{expense_id}`)

### 3. Set Up Environment Variables in Postman

For convenience, set up environment variables in Postman:
- `base_url`: The URL of your local server (e.g., `http://127.0.0.1:8000`)
- `access_token`: The access token you receive after logging in

### 4. Example Requests

**User Registration**

- Method: POST
- URL: `{{base_url}}/register/`
- Request Body (JSON):
    ```json
    {
        "username": "your_username",
        "email": "your_email@example.com",
        "password": "your_password"
    }
    ```

**User Login**

- Method: POST
- URL: `{{base_url}}/token`
- Request Body (form-data):
    - `username`: your username
    - `password`: your password

**Get Current User**

- Method: GET
- URL: `{{base_url}}/users/me/`
- Header:
    - `Authorization`: `Bearer {{access_token}}`

**Create Category**

- Method: POST
- URL: `{{base_url}}/categories/`
- Request Body (JSON):
    ```json
    {
        "name": "Category Name"
    }
    ```
- Header:
    - `Authorization`: `Bearer {{access_token}}`

**Create Expense**

- Method: POST
- URL: `{{base_url}}/expenses/`
- Request Body (JSON):
    ```json
    {
        "amount": 100.0,
        "description": "Groceries",
        "date": "2024-07-16",
        "category_id": 1
    }
    ```
- Header:
    - `Authorization`: `Bearer {{access_token}}`

### 5. Running Requests

Now you can run requests from the Postman collection to test your API. Ensure you update the environment variables and request headers with access tokens where necessary.

This process will help you quickly and efficiently test the API to ensure it is functioning correctly.


## Contributing

We welcome contributions to the Expense Tracker project. To contribute, please follow these guidelines:

### 1. Fork the Repository

- Navigate to the [Expense Tracker repository](https://github.com/VladPrime11/expensestracker).
- Click the "Fork" button in the top-right corner to create a copy of the repository under your GitHub account.

### 2. Clone the Forked Repository

Clone the forked repository to your local machine:

```bash
git clone https://github.com/VladPrime11/expensestracker.git
cd expensestracker


