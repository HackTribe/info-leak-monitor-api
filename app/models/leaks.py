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
from datetime import datetime

from app.db.base import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func


class Leak(Base):
    __tablename__ = "leaks"
    kind = Column(String(32), nullable=False)
    leakiest = Column(String(255), nullable=False)

    sha = Column(String(255), nullable=False)
    fragment = Column(Text, nullable=False)
    html_url = Column(String(512), nullable=False)
    last_modified = Column(DateTime,
                           default=datetime.now,
                           server_default=func.now())
    file_name = Column(String(512), nullable=False)
    repo_name = Column(String(120), nullable=False)
    repo_url = Column(String(512), nullable=False)
    user_avatar = Column(String(512))
    user_name = Column(String(255), nullable=False)
    user_url = Column(String(512), nullable=False)
    leak_count = Column(Integer, nullable=True, default=0)
    follow = Column(Boolean, nullable=True, default=False)
    ignore = Column(Boolean, nullable=True, default=False)
    is_white = Column(Boolean, nullable=True, default=False)
    is_process = Column(Boolean, nullable=True, default=False)
