from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import models
import schemas
import crud
import auth
import database

app = FastAPI()

# Dependency
async def get_db():
    async with database.AsyncSessionLocal() as session:
        yield session


@app.post("/api/register", response_model=schemas.UserRead)
async def register(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return await crud.create_user(db, user)


@app.post("/api/login", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await crud.get_user_by_username(db, form_data.username)
    if not user or not crud.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/api/posts", response_model=schemas.PostRead)
async def create_post(post: schemas.PostCreate, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return await crud.create_post(db, post, current_user.id)


@app.get("/api/posts", response_model=List[schemas.PostRead])
async def read_posts(db: AsyncSession = Depends(get_db)):
    return await crud.get_posts(db)


@app.get("/api/posts/{post_id}", response_model=schemas.PostRead)
async def read_post(post_id: int, db: AsyncSession = Depends(get_db)):
    post = await crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.put("/api/posts/{post_id}", response_model=schemas.PostRead)
async def update_post(post_id: int, post: schemas.PostUpdate, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_post = await crud.get_post(db, post_id)
    if not db_post or db_post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return await crud.update_post(db, post_id, post)


@app.delete("/api/posts/{post_id}")
async def delete_post(post_id: int, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_post = await crud.get_post(db, post_id)
    if not db_post or db_post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    await crud.delete_post(db, post_id)
    return {"detail": "Post deleted"}


@app.post("/api/posts/{post_id}/like")
async def like_post(post_id: int, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    like = await crud.like_post(db, post_id, current_user.id)
    if not like:
        raise HTTPException(status_code=400, detail="Already liked")
    return {"detail": "Post liked"}


@app.post("/api/posts/{post_id}/comment", response_model=schemas.CommentRead)
async def comment_post(post_id: int, comment: schemas.CommentCreate, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return await crud.comment_post(db, post_id, current_user.id, comment)


@app.get("/api/posts/{post_id}/comments", response_model=List[schemas.CommentRead])
async def get_comments(post_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_comments(db, post_id)
