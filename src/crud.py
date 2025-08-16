
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import models
import schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(
        select(models.User).where(models.User.username == username)
    )
    return result.scalars().first()

async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    return result.scalars().first()

async def create_post(db: AsyncSession, post: schemas.PostCreate, user_id: int):
    db_post = models.Post(**post.dict(), author_id=user_id)
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post

async def get_posts(db: AsyncSession):
    result = await db.execute(select(models.Post))
    return result.scalars().all()

async def get_post(db: AsyncSession, post_id: int):
    result = await db.execute(
        select(models.Post).where(models.Post.id == post_id)
    )
    return result.scalars().first()

async def update_post(db: AsyncSession, post_id: int, post: schemas.PostUpdate):
    db_post = await get_post(db, post_id)
    if db_post:
        db_post.title = post.title
        db_post.content = post.content
        await db.commit()
        await db.refresh(db_post)
    return db_post

async def delete_post(db: AsyncSession, post_id: int):
    db_post = await get_post(db, post_id)
    if db_post:
        await db.delete(db_post)
        await db.commit()
    return db_post

async def like_post(db: AsyncSession, post_id: int, user_id: int):
    result = await db.execute(
        select(models.Like).where(
            (models.Like.post_id == post_id) & (models.Like.user_id == user_id)
        )
    )
    existing_like = result.scalars().first()
    if existing_like:
        return None
    db_like = models.Like(post_id=post_id, user_id=user_id)
    db.add(db_like)
    await db.commit()
    await db.refresh(db_like)
    return db_like

async def comment_post(db: AsyncSession, post_id: int, user_id: int, comment: schemas.CommentCreate):
    db_comment = models.Comment(post_id=post_id, user_id=user_id, content=comment.content)
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment

async def get_comments(db: AsyncSession, post_id: int):
    result = await db.execute(
        select(models.Comment).where(models.Comment.post_id == post_id)
    )
    return result.scalars().all()
