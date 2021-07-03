#
# Copyright (C) 2021
#
# Author: hacktribe <hacktribe.org>
#
from typing import Any, List, Union, Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    subject: Union[str, Any]
    scopes: List[str] = []


class TokenInfo(BaseModel):
    kind: str
    access_token: str
    next_time: Optional[int] = 0

    class Config:
        orm_mode = True


class ResponseTokenInfo(TokenInfo):
    id: int
    create_time: int
    update_time: int

    class Config:
        orm_mode = True


class UpdateTokenInfo(TokenInfo):
    id: int

    class Config:
        orm_mode = True
