from typing import Union

from sqlalchemy import select

from api import schemas
from sqlalchemy.ext.asyncio import AsyncSession
from db import models

# DAL class implement crud operations
# DAL - Data Access Layer
from db.models import User
from hashing import Hasher


# TODO fix get methods
class Dal:
    """Data Access Layer for operating user info"""

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    # get by id
    async def get_user(self, user_id: int):
        return self.db.query(models.User).filter(models.User.id == user_id).first()

    # get by email
    async def get_user_by_email(self, email: str):
        return self.db.query(models.User).filter(models.User.email == email).first()

    # get by username
    async def get_user_by_username(self, username: str) -> Union[User, None]:
        query = select(User).where(User.username == username)
        result = await self.db.execute(query)
        user = result.fetchone()
        print(user)
        if user is not None:
            return user[0]
        # return await self.db.query(models.User).filter(models.User.username == username).first()

    async def get_users(self, skip: int = 0, limit: int = 100):
        return self.db.query(models.User).offset(skip).limit(limit).all()

    async def create_user(self, user: schemas.UserCreate) -> models.User:
        hashed_password = Hasher.get_password_hash(user.password)
        db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
        self.db.add(db_user)
        await self.db.flush()
        return db_user
