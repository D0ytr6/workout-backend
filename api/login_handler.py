from datetime import timedelta
from typing import Union

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status

import settings
from api.schemas import Token
from db.dals import Dal
from db.models import User
from db.session import get_db
from hashing import Hasher
from security import create_access_token

login_router = APIRouter()


async def _get_user_by_username_for_auth(username: str, db: AsyncSession):
    async with db as session:
        async with session.begin():
            user_dal = Dal(session)
            return await user_dal.get_user_by_username(
                username=username,
            )


async def authenticate_user(
        username: str, password: str, db: AsyncSession) -> Union[User, None]:
    user = await _get_user_by_username_for_auth(username=username, db=db)
    if user is None:
        return
    # if pass not equals to hashed form
    if not Hasher.verify_password(password, user.hashed_password):
        return
    return user


# request for getting token
# takes username and password from OAuth2Form - if user registered - token response
@login_router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "other_custom_data": [1, 2, 3, 4]},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}