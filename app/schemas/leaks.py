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
import datetime
from typing import List, Optional, Text

from pydantic import BaseModel


class LeakInfo(BaseModel):
    id: Optional[int]
    kind: Optional[str]
    leakiest: Optional[str]
    sha: Optional[str]
    fragment: Optional[Text]
    html_url: Optional[str]
    last_modified: Optional[datetime.datetime]
    file_name: Optional[str]
    repo_name: Optional[str]
    repo_url: Optional[str]
    user_avatar: Optional[str]
    user_name: Optional[str]
    user_url: Optional[str]
    leak_count: Optional[int]
    watching: Optional[bool]
    follow: Optional[bool]
    ignore: Optional[bool]
    is_white: Optional[bool]

    class Config:
        orm_mode = True


class LeakList(BaseModel):
    leaks: List[LeakInfo]

    class Config:
        orm_mode = True


class QueryLeak(BaseModel):
    kind: Optional[str]
    pages: Optional[int] = 1
    per_pages: Optional[int] = 10


class SearchLeak(BaseModel):
    kind: Optional[str]
    field: str
    keyword: str
    status: bool
    pages: Optional[int] = 1
    per_pages: Optional[int] = 10


class LeakState(BaseModel):
    id: int
    state_type: int
