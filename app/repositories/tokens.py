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

from . import Repository
from typing import Tuple, List
from app.models.tokens import GitAccessToken
from app.schemas.tokens import TokenInfo, UpdateTokenInfo


class TokenRepository(Repository):
    def add_token(self, token: TokenInfo) -> GitAccessToken:
        atoken = GitAccessToken(
            kind=token.kind.strip(),
            access_token=token.access_token.strip(),
            next_time=token.next_time,
        )
        self.db.add(atoken)
        self.db.commit()
        return atoken

    def modify_token(self, token: UpdateTokenInfo) -> GitAccessToken:
        token_info = (self.db.query(GitAccessToken).filter(
            GitAccessToken.id == token.id).first())
        if token_info:
            token_info.kind = token.kind
            token_info.access_token = token.access_token
            self.db.commit()
        return token_info

    def get_token_by_kind(self, kind: str) -> Tuple:
        total = (self.db.query(GitAccessToken).filter(
            GitAccessToken.kind == kind).count())
        data = self.db.query(GitAccessToken).filter(
            GitAccessToken.kind == kind).all()
        return (total, data)

    def get_tokens(self) -> Tuple:
        data = self.db.query(GitAccessToken).order_by(
            GitAccessToken.id.desc()).all()
        return (len(data), data)

    def set_next_time_by_access_token(self, access_token: str, next_time: int):
        self.db.query(GitAccessToken).filter(
            GitAccessToken.access_token == access_token).update(
                {"next_time": next_time})
        self.db.commit()

    def delete_token_by_ids(self, ids: List[int]):
        self.db.query(GitAccessToken).filter(
            GitAccessToken.id.in_(ids)).delete(synchronize_session=False)
        self.db.commit()
