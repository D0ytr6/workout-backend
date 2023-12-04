import uuid

from pydantic import BaseModel, EmailStr


# pydantic models for encapsulating request body or response body

class UserBase(BaseModel):
    username: str
    email: EmailStr


# add validation
class UserCreate(UserBase):
    password: str


# used as response model without password
class UserShow(UserBase):
    class Config:
        # convert obj to json
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


class TokenData(BaseModel):
    username: str | None = None
