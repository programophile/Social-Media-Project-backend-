from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
class PostCreate(PostBase):
    pass

class Post(BaseModel):
    title: str
    content: str
    id: int
    published: bool
    owner_id: int
    owner: "UserResponse"
    class Config:
        orm_mode = True
class UserCreate(BaseModel):
    email: EmailStr
    password: str
class UserResponse(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime
    class Config:
        orm_mode=True
class UserLogin(BaseModel):
    email: EmailStr
    password: str
class Token(BaseModel):
    access_token: str
    token_type:str
class TokenData(BaseModel):
    id: Optional[int]=None

class Vote(BaseModel):
    post_id:int
    dir: int = Field(..., ge=-1, le=1)

class PostOut(BaseModel):
    Post: Post
    votes: int
    class Config:
        orm_mode=True