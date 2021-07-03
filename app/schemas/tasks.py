#
# Copyright (C) 2021, hacktribe
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
from typing import List, Optional, Union

from pydantic import BaseModel


class TaskInfo(BaseModel):
    kind: Optional[str]
    name: Optional[str]
    runtime_type: Optional[int]
    runtime: Union[int, str]
    pages: Optional[int]
    keywords: Optional[List[str]]
    excludes: Optional[List[str]]

    class Config:
        orm_mode = True


class ResponseTaskInfo(TaskInfo):
    id: Optional[str]

    class Config:
        orm_mode = True


class UpdateTaskInfo(ResponseTaskInfo):
    class Config:
        orm_mode = True


class WhiteListInfo(BaseModel):
    kind: str
    sha: str
    url_path: str
    url_path_last_time: Optional[datetime.datetime]

    class Config:
        orm_mode = True


class ResponseWhiteListInfo(WhiteListInfo):
    id: Optional[int]

    class Config:
        orm_mode = True
