#
# Copyright (C) 2021
#
# Author: hacktribe <hacktribe.org>
#

from typing import Optional

from pydantic import BaseModel


class UserInfo(BaseModel):
    username: str
    email: Optional[str]

    class Config:
        orm_mode = True


class UserRegister(UserInfo):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str
