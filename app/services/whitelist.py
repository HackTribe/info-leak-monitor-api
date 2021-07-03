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
from typing import Tuple
from fastapi import Depends
from app.repositories.whitelist import WhiteListRepository
from app.schemas.tasks import WhiteListInfo
from app.models.whitelist import WhiteList


class WhiteListService(object):
    whitelist_repo: WhiteListRepository

    def __init__(
        self,
        whitelist_repo: WhiteListRepository = Depends(WhiteListRepository)):
        self.whitelist_repo = whitelist_repo

    def add(self, whitelist: WhiteListInfo) -> WhiteList:
        return self.whitelist_repo.add_whitelist(whitelist)

    def is_existed(self, sha: str) -> bool:
        if self.whitelist_repo.is_existed(sha) != None:
            return True
        return False

    def get_whitelist_by_kind(self, kind: str, per: int, page: int) -> Tuple:
        return self.whitelist_repo.get_whitelist_by_kind(kind, per, page)

    def get_whitelist_sha_by_kind(self, kind: str) -> Tuple:
        return self.whitelist_repo.get_whitelist_sha_by_kind(kind)

    def get_whitelists(self, per: int, page: int) -> Tuple:
        return self.whitelist_repo.get_whitelists(per, page)

    def delete_whitelist_by_id(self, id: int):
        self.whitelist_repo.remove_whitelist_by_id(id)

    def get_whitelist_by_id(self, id: int) -> WhiteList:
        return self.whitelist_repo.get_whitelist_by_id(id)
