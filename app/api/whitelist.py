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
from typing import List
import math
from fastapi import APIRouter, Depends, Security, Response

from app.core.security import verify_access_token
from app.services.leaks import LeakService
from app.services.whitelist import WhiteListService
from app.schemas.tasks import WhiteListInfo, ResponseWhiteListInfo
from app.schemas.leaks import LeakState
from app.core.security import verify_access_token

router = APIRouter(
    prefix="", dependencies=[Security(verify_access_token, scopes=["api"])])


@router.post("/whitelist", response_model=ResponseWhiteListInfo)
def add_whitelist(
        wlist: WhiteListInfo,
        leak_service: LeakService = Depends(LeakService),
        whitelist_service: WhiteListService = Depends(WhiteListService),
):

    whitelist = whitelist_service.add(wlist)
    if whitelist:
        leak_state = LeakState(state_type=1, id=whitelist.id)
        leak_service.process(leak_state)
    return whitelist


@router.delete("/whitelist/{id}", response_model=WhiteListInfo)
def remove_whitelist(
        id: int,
        whitelist_service: WhiteListService = Depends(WhiteListService),
):
    return whitelist_service.delete_whitelist_by_id(id)


@router.get("/whitelists/{kind}", response_model=List[ResponseWhiteListInfo])
def get_whitelist(
        kind: str,
        response: Response,
        per: int = 10,
        page: int = 1,
        whitelist_service: WhiteListService = Depends(WhiteListService),
):
    total, data = whitelist_service.get_whitelist_by_kind(kind, per, page)
    response.headers.update({
        "X-Total-Count": str(total),
        "X-Total-Pages": str(math.ceil(total / per)),
    })
    return data


@router.get("/whitelists", response_model=List[ResponseWhiteListInfo])
def get_whitelist_all(
        response: Response,
        per: int = 10,
        page: int = 1,
        whitelist_service: WhiteListService = Depends(WhiteListService),
):
    total, data = whitelist_service.get_whitelists(per, page)
    response.headers.update({
        "X-Total-Count": str(total),
        "X-Total-Pages": str(math.ceil(total / per)),
    })
    return data
