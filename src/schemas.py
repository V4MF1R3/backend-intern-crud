from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    model_config = {
        "from_attributes": True
    }

class Token(BaseModel):
    access_token: str
    token_type: str

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class PostRead(PostBase):
    id: int
    author_id: int
    created_at: datetime
    model_config = {
        "from_attributes": True
    }

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class CommentRead(CommentBase):
    id: int
    user_id: int
    post_id: int
    created_at: datetime
    model_config = {
        "from_attributes": True
    }
