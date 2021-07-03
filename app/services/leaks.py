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
from app.repositories.leaks import LeakRepository
from app.repositories.whitelist import WhiteListRepository
from app.schemas.leaks import QueryLeak, SearchLeak, LeakInfo, LeakState
from app.models.leaks import Leak
from app.schemas.tasks import WhiteListInfo


class LeakService(object):
    leak_repo: LeakRepository
    whitelist_repo: WhiteListRepository

    def __init__(
            self,
            leak_repo: LeakRepository = Depends(LeakRepository),
            whitelist_repo: WhiteListRepository = Depends(LeakRepository),
    ):
        self.leak_repo = leak_repo

    def add(self, leak: LeakInfo) -> Leak:
        return self.leak_repo.add(leak)

    def is_leak(self, sha: str) -> Leak:
        return self.leak_repo.get_leak_by_sha(sha)

    def search_leaks(self, query: SearchLeak) -> Tuple:
        return self.leak_repo.search_leaks(query)

    def get_leaks(self, query: QueryLeak) -> Tuple:
        if query.per_pages is None:
            per = 10
        else:
            per = query.per_pages
        if query.pages is None:
            page = 1
        else:
            page = query.pages
        return self.leak_repo.get_leaks(query.kind, per, page)

    def get_all_export(self, kind: str) -> Tuple:
        return self.leak_repo.get_all_export(kind)

    def process(self, leak_state: LeakState):
        if leak_state.state_type == 0:
            self.leak_repo.set_ignore(leak_state.id)
        elif leak_state.state_type == 1:
            leak = self.leak_repo.get_leak_by_id(leak_state.id)
            if leak:
                whitelist = WhiteListInfo(
                    kind=leak.kind,
                    sha=leak.sha,
                    url_path=leak.repo_url,
                    url_path_last_time=leak.last_modified,
                )
                self.whitelist_repo.add_whitelist(whitelist)
            self.leak_repo.set_whitelist(leak_state.id)
        else:
            self.leak_repo.set_process(leak_state.id)
