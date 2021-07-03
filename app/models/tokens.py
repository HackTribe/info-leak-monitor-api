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

from app.db.base import Base
from sqlalchemy import Column, String, BigInteger


class GitAccessToken(Base):
    __tablename__ = "git_access_tokens"
    kind = Column(String(32), nullable=False)
    access_token = Column(String(255), nullable=False)
    next_time = Column(BigInteger, nullable=False)
