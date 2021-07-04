#
# Copyright (C) 2021 hacktribe
#
# Author: hacktribe <hacktribe.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
import math
from starlette.status import HTTP_403_FORBIDDEN
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, Security
from app.services.tokens import TokenService
from app.schemas.tokens import TokenInfo, ResponseTokenInfo, UpdateTokenInfo
from app.core.security import verify_access_token

router = APIRouter(
    prefix="", dependencies=[Security(verify_access_token, scopes=["api"])])


@router.get("/git-access-tokens", response_model=List[ResponseTokenInfo])
def get_tokens(response: Response,
               token_service: TokenService = Depends(TokenService)):
    total, data = token_service.get_access_tokens()
    new_data = []
    for d in data:
        d.access_token = d.access_token[0:math.floor(
            len(d.access_token) / 2 /
            2)] + "******" + d.access_token[math.floor(-len(d.access_token) /
                                                       2 / 2):]
        new_data.append(d)
    response.headers.update({
        "X-Total-Count": str(total),
    })
    return new_data


@router.get("/git-access-tokens/{kind}",
            response_model=List[ResponseTokenInfo])
def get_token_by_kind(kind: str,
                      response: Response,
                      token_service: TokenService = Depends(TokenService)):
    total, data = token_service.get_access_tokens_by_kind(kind)
    new_data = []
    for d in data:
        d.access_token = d.access_token[0:math.floor(
            len(d.access_token) / 2 /
            2)] + "******" + d.access_token[math.floor(-len(d.access_token) /
                                                       2 / 2):]
        new_data.append(d)
    response.headers.update({
        "X-Total-Count": str(total),
    })

    return new_data


@router.post("/git-access-token", response_model=ResponseTokenInfo)
def add_access_token(tlist: TokenInfo,
                     token_service: TokenService = Depends(TokenService)):
    token = token_service.add_access_token(tlist)
    if token:
        return token
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN,
        detail="修改失败！",
    )


@router.put("/git-access-token", response_model=ResponseTokenInfo)
def modify_access_token(tlist: UpdateTokenInfo,
                        token_service: TokenService = Depends(TokenService)):
    token = token_service.modify_access_token(tlist)
    if token:
        return token
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN,
        detail="修改失败！",
    )


@router.delete("/git-access-token")
def remove_access_token(ids: List[int],
                        token_service: TokenService = Depends(TokenService)):
    return token_service.delete_access_token_by_ids(ids)
