#
# Copyright (C) 2021
#
# Author: hacktribe <hacktribe.org>
#
import re
from typing import Optional
from pydantic import BaseModel, validator


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


class ModifyUserPassword(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str

    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        def is_valid(password):
            if len(password) < 6 or len(password) > 20:
                return False
            if not re.search("[a-z]", password):
                return False
            if not re.search("[A-Z]", password):
                return False
            if not re.search("\d", password):
                return False
            return True

        if not is_valid(v):
            raise ValueError("密码长度必须大于6位，包含大写字母数字！")
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('新密码与确认密码不一致！')
        return v
