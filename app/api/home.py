#
# Copyright (C) 2021 hacktribe
#
# Author: hacktribe <hacktribe.org>
#

from app.core.security import create_access_token, verify_access_token
from app.services.user import UserService
from app.schemas.tokens import Token
from app.schemas.user import UserInfo, UserLogin, UserRegister
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

router = APIRouter()
user = APIRouter(prefix="/user",
                 dependencies=[Security(verify_access_token, scopes=["api"])])


@router.post("/register", response_model=UserInfo)
async def register(userinfo: UserRegister,
                   user_service: UserService = Depends(UserService)):
    try:

        user = user_service.create(userinfo)

        return {
            "username": user.username,
            "email": user.email,
        }

    except HTTPException as e:
        logger.error(e)
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal Server Error")


@user.get("/me", response_model=UserInfo)
async def info(
        current_user: str = Depends(verify_access_token),
        user_service: UserService = Depends(UserService),
):
    return user_service.get_current_user(current_user)


@router.post("/login", response_model=Token)
async def login_for_access_token(
        form_data: UserLogin,
        user_service: UserService = Depends(UserService),
):
    try:
        user = user_service.authenticate(form_data.username,
                                         form_data.password)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal Server Error")

    if not user:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")

    access_token = create_access_token(data={
        "sub": user.username,
        "scopes": ["api"]
    })
    return {"access_token": access_token, "token_type": "Bearer"}


@router.post("/settings/tokens", response_model=Token)
async def personal_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        user_service: UserService = Depends(UserService),
):
    try:
        user = user_service.authenticate(form_data.username,
                                         form_data.password)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal Server Error")

    if not user:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")

    if len(form_data.scopes) == 0:
        form_data.scopes = ["api"]
    access_token = create_access_token(data={
        "sub": user.username,
        "scopes": form_data.scopes
    })
    return {"access_token": access_token, "token_type": "Bearer"}


@router.post("/status")
async def get_status():
    return {"status": "ok"}
