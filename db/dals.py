from api import schemas
from sqlalchemy.ext.asyncio import AsyncSession
from db import models


# DAL class implement crud operations
# DAL - Data Access Layer


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

    async def get_users(self, skip: int = 0, limit: int = 100):
        return self.db.query(models.User).offset(skip).limit(limit).all()

    async def create_user(self, user: schemas.UserCreate) -> models.User:
        fake_hashed_password = user.password + "notreallyhashed"
        db_user = models.User(username=user.nick_name, email=user.email, hashed_password=fake_hashed_password)
        self.db.add(db_user)
        await self.db.flush()
        return db_user
