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

import base64
import csv
import time
import math
from typing import List
from starlette.responses import FileResponse
from fastapi import APIRouter, Depends, Security, Response
from app.services.leaks import LeakService
from app.schemas.leaks import LeakInfo, QueryLeak, SearchLeak, LeakState
from app.core.security import verify_access_token

router = APIRouter(
    prefix="", dependencies=[Security(verify_access_token, scopes=["api"])])


@router.post("/leaks/search", response_model=List[LeakInfo])
def search(
        query: SearchLeak,
        response: Response,
        leak_service: LeakService = Depends(LeakService),
):

    total, data = leak_service.search_leaks(query)
    response.headers.update({
        "X-Total-Count":
        str(total),
        "X-Total-Pages":
        str(math.ceil(total / query.per_pages)),
    })
    return data


@router.get("/leaks/lists/{kind}", response_model=List[LeakInfo])
def get_leaks(
        kind: str,
        per: int,
        page: int,
        response: Response,
        leak_service: LeakService = Depends(LeakService),
):
    query = QueryLeak(kind=kind, per_pages=per, pages=page)
    total, data = leak_service.get_leaks(query)
    response.headers.update({
        "X-Total-Count": str(total),
        "X-Total-Pages": str(math.ceil(total / per)),
    })
    return data


@router.patch("/leaks")
def process_leaks(leak_state: LeakState,
                  leak_service: LeakService = Depends(LeakService)):

    return leak_service.process(leak_state)


@router.post("/leaks/export")
def export_csv_file(query: SearchLeak,
                    leak_service: LeakService = Depends(LeakService)):
    export_csv = f"./download/{time.time()}.csv"

    _, result = leak_service.search_leaks(query)

    with open(export_csv, "w", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow([
            "id",
            "kind",
            "leakiest",
            "sha",
            "fragment",
            "html_url",
            "last_modified",
            "file_name",
            "repo_name",
            "repo_url",
            "user_avatar",
            "user_name",
            "user_url",
            "leak_count",
            "is_process",
            "ignore",
            "is_white",
        ])

        if result is None:
            return FileResponse(export_csv)

        for data in result:
            writer.writerow([
                data.id,
                data.kind,
                data.leakiest.encode("utf-8"),
                data.sha,
                base64.b64encode(data.fragment.encode("utf-8")),
                data.html_url.encode("utf-8"),
                data.last_modified,
                data.file_name.encode("utf-8"),
                data.repo_name.encode("utf-8"),
                data.repo_url.encode("utf-8"),
                data.user_avatar,
                data.user_name.encode("utf-8"),
                data.user_url.encode("utf-8"),
                data.leak_count,
                data.is_process,
                data.ignore,
                data.is_white,
            ])

    return FileResponse(export_csv)
