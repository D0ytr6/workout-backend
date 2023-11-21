from pydantic import BaseModel

# pydantic models for encapsulating request body

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str

# used as response model without password
class User(UserBase):
    id: int

    class Config:
        orm_mode = True
