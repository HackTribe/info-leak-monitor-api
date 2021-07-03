#
# Copyright (C) 2021 hacktribe
#
# Author: hacktribe <hacktribe.org>
#

from app.schemas.user import UserRegister
from app.repositories.user import UserRepository
from app.models.user import User
from fastapi import Depends, HTTPException
from starlette.status import (
    HTTP_403_FORBIDDEN, )


class UserService(object):
    user_repo: UserRepository

    def __init__(self, user_repo: UserRepository = Depends(UserRepository)):
        self.user_repo = user_repo

    def get_current_user(self, username: str) -> User:
        if not username is None:
            return self.user_repo.get_by_username(username)

        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="{} Not Found.".format(username),
        )

    def authenticate(self, username: str, password: str) -> User:
        return self.user_repo.authenticate(username, password)

    def create(self, user_register: UserRegister) -> User:
        user = self.user_repo.get_by_username(user_register.username)
        if user:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="'{0}' existed, register failed. ".format(
                    user_register.username),
            )
        else:
            user = self.user_repo.create(user_register)

        return user
