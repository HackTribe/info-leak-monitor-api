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

from typing import List, Tuple
from app.models.whitelist import WhiteList
from app.schemas.tasks import WhiteListInfo
from . import Repository


class WhiteListRepository(Repository):
    def add_whitelist(self, wlist: WhiteListInfo) -> WhiteList:
        wl = WhiteList(
            sha=wlist.sha,
            kind=wlist.kind,
            url_path=wlist.url_path,
            url_path_last_time=wlist.url_path_last_time,
        )
        if not self.is_existed(wlist.sha):
            self.db.add(wl)
            self.db.commit()
        return wl

    def is_existed(self, sha: str) -> bool:
        has = self.db.query(WhiteList).filter(WhiteList.sha == sha).first()
        if has:
            return True
        return False

    def get_whitelist_by_kind(self, kind: str, per: int, page: int) -> Tuple:
        per, page = self.get_offset(per, page)
        data = (self.db.query(WhiteList).filter(
            WhiteList.kind == kind).offset(page).limit(per).all())

        total = self.db.query(WhiteList).filter(WhiteList.kind == kind).count()
        return (total, data)

    def get_whitelist_sha_by_kind(self, kind: str) -> Tuple:
        whitelists = self.db.query(WhiteList).filter(
            WhiteList.kind == kind).all()
        result = [wl.sha for wl in whitelists]
        total = self.db.query(WhiteList).filter(WhiteList.kind == kind).count()
        return (total, result)

    def get_whitelists(self, per: int, page: int) -> Tuple:
        per, page = self.get_offset(per, page)
        data = self.db.query(WhiteList).offset(page).limit(per).all()
        total = self.db.query(WhiteList).count()
        return (total, data)

    def remove_whitelist_by_id(self, id: int):
        self.db.query(WhiteList).filter(WhiteList.id == id).delete()
        self.db.commit()

    def get_whitelist_by_id(self, id: int) -> WhiteList:
        return self.db.query(WhiteList).filter(WhiteList.id == id).first()
