from datetime import timedelta, datetime
from typing import Union, Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status

import settings
from api.schemas import Token, TokenData
from db.dals import Dal
from db.models import User
from db.session import get_db
from hashing import Hasher
from security import create_access_token

login_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


async def get_current_user_is_admin(token: str = Depends(oauth2_scheme),
                                      db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You are not administrator",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        is_admin: bool = payload.get("isAdmin")
        username: str = payload.get("sub")
        if is_admin is False:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await _get_user_by_username_for_auth(username=username, db=db)
    if user is None:
        raise credentials_exception
    return user


async def get_current_user_from_token(token: str = Depends(oauth2_scheme),
                                      db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await _get_user_by_username_for_auth(username=username, db=db)
    if user is None:
        raise credentials_exception
    return user


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

    # Generate new access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, },
        expires_delta=access_token_expires,
    )

    # Generate a new refresh token
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_access_token(
        data={"sub": user.username, },
        expires_delta=refresh_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}


# Endpoint to refresh the access token using a refresh token
@login_router.post("/token/refresh")
def refresh_access_token(refresh_token: str = Depends(OAuth2PasswordBearer(tokenUrl="refresh_token"))):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Generate a new access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username, },
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


# token resource
@login_router.get("/me")
async def read_users_me(
        current_user: User = Depends(get_current_user_from_token),
):
    return {"Success": True, "current_user": current_user}


# token resource
@login_router.get("/admin")
async def read_admin_me(
        current_admin: User = Depends(get_current_user_is_admin),
):
    return {"Success": True, "current_user": current_admin}