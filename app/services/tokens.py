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
from typing import Tuple, List
from fastapi import Depends
from app.repositories.tokens import TokenRepository
from app.schemas.tokens import TokenInfo, UpdateTokenInfo
from app.models.tokens import GitAccessToken


class TokenService(object):
    token_repo: TokenRepository

    def __init__(self, token_repo: TokenRepository = Depends(TokenRepository)):
        self.token_repo = token_repo

    def add_access_token(self, token: TokenInfo) -> GitAccessToken:
        return self.token_repo.add_token(token)

    def modify_access_token(self, token: UpdateTokenInfo) -> GitAccessToken:
        return self.token_repo.modify_token(token)

    def get_access_tokens(self) -> Tuple:
        return self.token_repo.get_tokens()

    def get_access_tokens_by_kind(self, kind: str) -> Tuple:
        return self.token_repo.get_token_by_kind(kind)

    def set_next_time_by_access_token(self, access_token: str, next_time: int):
        return self.token_repo.set_next_time_by_access_token(
            access_token, next_time)

    def delete_access_token_by_ids(self, ids: List):
        return self.token_repo.delete_token_by_ids(ids)
