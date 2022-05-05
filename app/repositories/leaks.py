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

from app.models.leaks import Leak
from app.schemas.leaks import LeakInfo, SearchLeak
from . import Repository
from sqlalchemy import func, or_


class LeakRepository(Repository):

    def add(self, leak: LeakInfo) -> Leak:
        leakinfo = Leak(
            kind=leak.kind,
            leakiest=leak.leakiest,
            sha=leak.sha,
            fragment=leak.fragment,
            html_url=leak.html_url,
            last_modified=leak.last_modified,
            file_name=leak.file_name,
            repo_name=leak.repo_name,
            repo_url=leak.repo_url,
            user_avatar=leak.user_avatar,
            user_name=leak.user_name,
            user_url=leak.user_url,
            leak_count=0,
            follow=0,
            is_process=0,
        )

        self.db.add(leakinfo)
        self.db.commit()
        return leakinfo

    def get_leak_by_sha(self, sha: str) -> Leak:
        return self.db.query(Leak).filter(Leak.sha == sha).first()

    def get_leak_by_id(self, id: int) -> Leak:
        return self.db.query(Leak).filter(Leak.id == id).first()

    def search_leaks(self, query: SearchLeak) -> Tuple:
        if query.per_pages:
            per = query.per_pages
        else:
            per = self.per
        if query.pages:
            page = query.pages
        else:
            page = 1
        per_page, pages = self.get_offset(per, page)

        querys = []
        if query.kind:
            if query.kind.lower() != "all":
                querys.append(Leak.kind == query.kind.lower())
        if query.field.lower() == "leakiest":
            querys.append(Leak.leakiest == query.keyword)

        elif query.field.lower() == "user_name":
            querys.append(func.instr(query.keyword, Leak.user_name))

        elif query.field.lower() == "repo_name":
            querys.append(
                or_(
                    func.instr(query.keyword, Leak.repo_name),
                    func.instr(query.keyword, Leak.repo_url),
                ))
        if query.state_type == 0:
            querys.append(Leak.ignore != 0)
        elif query.state_type == 1:
            querys.append(Leak.is_white != 0)
        elif query.state_type == 2:
            querys.append(Leak.is_process != 0)
        count = self.db.query(Leak).filter(*querys).count()
        data = (self.db.query(Leak).filter(*querys).order_by(
            Leak.id.desc()).offset(pages).limit(per_page).all())
        return (count, data)

    def get_leaks(self,
                  kind: str = None,
                  per: int = 10,
                  page: int = 1) -> Tuple:
        per_page, pages = self.get_offset(per, page)
        querys = [Leak.ignore == 0, Leak.is_white == 0, Leak.is_process == 0]
        if kind:
            querys.append(Leak.kind == kind)

        count = self.db.query(Leak).filter(*querys).count()
        data = (self.db.query(Leak).filter(*querys).order_by(
            Leak.id.desc()).offset(pages).limit(per_page).all())
        return (count, data)

    def get_all_export(self, kind: str) -> Tuple:
        querys = [Leak.ignore == 0, Leak.is_white == 0]
        if kind.lower() != "all":
            querys.append(Leak.kind == kind.lower())
        count = self.db.query(Leak).filter(*querys).count()
        data = self.db.query(Leak).filter(*querys).all()
        return (count, data)

    def set_ignore(self, id: int, flag: int = 1):
        leak = self.db.query(Leak).filter(Leak.id == id).first()
        if leak:
            leak.ignore = flag
            self.db.commit()

    def set_process(self, id: int, flag: int = 1):
        leak = self.db.query(Leak).filter(Leak.id == id).first()
        if leak:
            leak.is_process = flag
            self.db.commit()

    def set_whitelist(self, id: int, flag: int = 1):
        leak = self.db.query(Leak).filter(Leak.id == id).first()
        if leak:
            leak.is_white = flag
            self.db.commit()

    def set_whitelist_by_sha(self, sha: str, flag: int = 0):
        leak = self.db.query(Leak).filter(Leak.sha == sha).first()
        if leak:
            leak.is_white = flag
            self.db.commit()
