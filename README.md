# Backend Intern Assignment: Blog Post CRUD Operations

This project is a FastAPI-based backend for a blog management system, supporting CRUD operations, likes, comments, and JWT authentication.

## Features
- User registration and login (JWT-based authentication)
- Create, read, update, and delete blog posts
- Like posts (one like per user per post)
- Comment on posts and fetch comments
- All write operations are protected by authentication
- Async SQLAlchemy support with Alembic migrations

## Setup Instructions

### 1. Clone the Repository
```
git clone <your-repo-url>
cd backend-intern-crud
```

### 2. Create and Activate a Virtual Environment
```
python -m venv .venv
.venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```

### 4. Run Alembic Migrations
```
alembic upgrade head
```

### 5. Start the FastAPI Server
```
uvicorn src.main:app --reload
```

The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000)

## API Endpoints
- `POST   /api/register`         - Register a new user
- `POST   /api/login`            - Login and get JWT token
- `POST   /api/posts`            - Create a blog post (auth required)
- `GET    /api/posts`            - Get all blog posts
- `GET    /api/posts/{id}`       - Get a single blog post by ID
- `PUT    /api/posts/{id}`       - Update a blog post (auth required)
- `DELETE /api/posts/{id}`       - Delete a blog post (auth required)
- `POST   /api/posts/{id}/like`  - Like a post (auth required)
- `POST   /api/posts/{id}/comment` - Add a comment (auth required)
- `GET    /api/posts/{id}/comments` - Get comments for a post

## Postman Collection
A sample Postman collection is provided in the repository root as `postman_collection.json`.

