from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from api import schemas

# models - sqlalchemy models, working with database orm
# schemas - pydantic models, validate data

from api.schemas import UserCreate, UserShow
from db.dals import Dal
from db.session import get_db

# router for operation with user
user_router = APIRouter()

# TODO save hashed password
# TODO add hashing methods
# TODO add logging
# TODO add validator, regex

# shadow logic
async def _create_user(body: UserCreate, db: AsyncSession) -> UserShow:
    async with db as session:
        async with session.begin():
            dal = Dal(db_session=session)
            user = await dal.create_user(body)
            return UserShow(
                user_id=user.id,
                username=user.username,
                email=user.email
            )


@user_router.post("/register/", response_model=schemas.UserShow)
async def create_user(body: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await _create_user(body, db)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


# @user_router.get("/users/", response_model=list[schemas.UserShow])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users
#
#
# @user_router.get("/users/{user_id}", response_model=schemas.UserShow)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user
